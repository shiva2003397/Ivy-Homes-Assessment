In the script, the database schema used in the MongoDB collection "Movies" for storing IMDb movie details consists of the following structure:

json
Copy code
{
  "Genre": "String",
  "List of Movies": [
    {
      "Title": "String",
      "Year Of Release": "String",
      "Director": "String",
      "Cast": ["String"],
      "Reviews": [
        {
          "Rating": "String",
          "Content": "String",
          "Date": "String"
        },
        // Additional review objects (up to 10) for each movie
      ]
    },
    // Additional movie objects for each genre
  ]
}
Here's a breakdown of the schema:

- Genre: String field representing the movie genre.
  
- List of Movies: Array containing movie objects for each genre.
  
- Title: String field representing the movie title.
  
- Year Of Release: String field representing the year of movie release.
  
- Director: String field representing the movie director.
  
- Cast: Array of strings containing the names of the cast members.
  
- Reviews: Array of review objects for each movie.
  
- Rating: String field representing the movie's rating out of 10.
  
- Content: String field containing the review content.
  
- Date: String field representing the date of the review.
  
This schema organizes the movie details retrieved from IMDb into a MongoDB collection, structured by genre and including movie-specific details like title, release year, director, cast members, and up to 10 latest reviews per movie.
