# IMDb Top Movies Scraper

## Purpose
This Python script is designed to scrape IMDb for the top 20 movies across various genres and store their details, including movie title, year of release, director, cast, and 10 latest reviews, into a MongoDB database. It utilizes web scraping techniques to extract data from IMDb's website and uses concurrent processing for efficient scraping.

## Setup Instructions

### Prerequisites
- Python 3.x installed
- MongoDB installed (or access to a MongoDB instance)

### Installation
1. Clone this repository or download the script (`main.py`) to your local machine.

2. Install the required Python dependencies using pip:
   ```bash
   pip install requests beautifulsoup4 pymongo
   ```

## Configuration
- Ensure you have MongoDB installed and running, or have access to a MongoDB instance. Update the `mongourl` variable in the script (`main.py`) with your MongoDB connection string.

## Execution Instructions
1. Open the terminal/command prompt.

2. Navigate to the directory where the `main.py` script is located.

3. Run the script using the following command:
   ```bash
   python main.py
   ```

## Important Considerations
- This script relies on web scraping IMDb's website, which is subject to change. If IMDb's website structure or layout changes, the script may need modifications to function correctly.
 
- IMDb's website usage policy should be adhered to while running this script to avoid any legal issues.
  
- The script scrapes data concurrently using ThreadPoolExecutor to enhance performance. Adjust the `max_workers` parameter in `getData()` if needed, considering system capabilities and network constraints.

---

## Explanation of functions in the code:

- getData(): This function serves as the main entry point. It establishes a connection to a MongoDB database and gets a list of movie genres using getGenres(). Then, it uses a ThreadPoolExecutor to concurrently process each genre using the processGenre() function.

- processGenre(genre, collection): This function takes a genre and a MongoDB collection as input. It fetches a list of movies for a specific genre using getMovies(genre) and then inserts the data (genre and list of movies) into the MongoDB collection.

- getSoupFromUrl(URL): This function uses the requests library to make an HTTP GET request to a given URL with a custom user-agent header. It then uses BeautifulSoup to parse the HTML content and returns the BeautifulSoup object representing the parsed HTML.

- getGenres(): This function scrapes the IMDb website to retrieve a list of movie genres by accessing the genre page. It extracts the genre names and returns them as a list.

- getMovies(genre): This function takes a genre as input, constructs a URL specific to that genre on IMDb, scrapes the webpage to get the top 20 movies for that genre, and returns a list of movie details by calling getMovieDetails(id) for each movie.

- getMovieDetails(id): This function fetches details for a specific movie by its IMDb ID. It extracts information such as movie title, year of release, director, cast, and reviews. It then constructs a dictionary containing these details and returns it.

- getRating(s): This is a helper function used to extract and format the movie rating from a string. It parses the rating from the string and returns it in the format "X/10".

- getReviews(id): This function fetches the top 10 latest reviews for a specific movie by its IMDb ID. It extracts review details like rating, content, and date, constructs a list of dictionaries containing this information, and returns it.
