from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def getData():
    client = MongoClient("mongodb://localhost:27017")

    db = client["IMDBTopMovies"]
    collection = db["Movies"]

    genres = getGenres()

    with ThreadPoolExecutor(max_workers=8) as executor:
        for genre in genres:
            executor.submit(processGenre, genre, collection)

    return


def processGenre(genre, collection):
    data = {
        "Genre": genre,
        "List of Movies": getMovies(genre)
    }
    collection.insert_one(data)
    return
        

def getSoupFromUrl(URL):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(URL , headers=headers)

    soup = BeautifulSoup(r.text , 'html.parser')
    return soup

def getGenres():
    soup = getSoupFromUrl('https://m.imdb.com/feature/genre/')
    
    #This List contains all movie tags
    movieGenreTags = soup.find_all("div", class_="ipc-chip-list__scroller")[1].find_all("a")

    genres = []
    for i in movieGenreTags:
        genres.append(i.text)

    return genres

def getMovies(genre):
    # URL of any movie type depends on the its type
    soup = getSoupFromUrl('https://m.imdb.com/search/title/?title_type=feature&genres='+genre)
    
    allMovies = soup.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-315eec58-0 hvFmRn detailed-list-view ipc-metadata-list--base").find_all("li")

    movies = []
    limit = 20

    for i in allMovies[:min(limit, len(allMovies))]:
        MovieID = i.find("a", class_="ipc-title-link-wrapper")["href"].split("?")[0]
        movies.append(getMovieDetails(MovieID))


    return movies

def getMovieDetails(id):
    soup = getSoupFromUrl('https://m.imdb.com'+id)

    # print('https://m.imdb.com'+id)

    movieTitle = soup.find("span", class_="hero__primary-text")
    if(movieTitle):
        movieTitle = movieTitle.text
    else:
        movieTitle = ""

    movieYOR = soup.find("ul", class_="ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt")
    if(movieYOR):
        movieYOR = movieYOR.find_all("a")[0].text
    else:
        movieYOR = ""

    movieDirector = soup.find("a", class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
    if(movieDirector):
        movieDirector = movieDirector.text
    else:
        movieDirector = ""

    movieCast = []
    cast = soup.find("div", class_="ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l ipc-shoveler__grid")
    if(cast):
        cast = cast.find_all("a" , class_ = "sc-bfec09a1-1 gCQkeh")
        for c in cast:
            movieCast.append(c.text)
    else:
        cast = []

    movieReviews = getReviews(id)

    movieData = {
        "Title": movieTitle,
        "Year Of Release": movieYOR,
        "Director": movieDirector,
        "Cast": movieCast,
        "Reviews": movieReviews
    }

    return movieData


def getRating(s):
    ans = ""
    for ch in s:
        if(ch.isnumeric()): 
            ans = ch
            break
    
    ans += "/10"
    return ans

def getReviews(id):
    soup = getSoupFromUrl('https://m.imdb.com'+id+'reviews?sort=submissionDate&dir=desc')
    # print('https://m.imdb.com'+id+'reviews?sort=submissionDate&dir=desc')

    allReviews = soup.find_all(class_ = "ipl-content-list__item")

    reviews = []
    limit = 0

    for i in allReviews:

        limit += 1
        if(limit > 10): break
    
        date = i.find("span", class_="review-date")
        if(date): date = date.text
        else: date = ""

        content = i.find("div", class_="content")
        if(content): content = content.find("div", class_="text").text
        else: content = ""

        rating = i.find("span", class_="rating-other-user-rating")
        if(rating): rating = getRating(rating.text)
        else: rating = "None"

        review = {
            "Rating": rating,
            "Content": content,
            "Date": date
        }

        reviews.append(review)
    
    return reviews


# getData()



# getMovies("Documentary")
