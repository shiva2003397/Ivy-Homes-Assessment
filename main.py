import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def getData():
    client = MongoClient("mongodb://localhost:27017")

    db = client["IMDBTopMovies"]
    collection = db["Movies"]

    genres = getGenres()

    for genre in genres:
        data = {
            "Genre": genre,
            "List of Movies": getMovies(genre)
        }
        collection.insert_one(data)

    return