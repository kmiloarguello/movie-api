from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"
app.description = "This is a very fancy movie API"

movies = [
    {
      "id": 1,
      "title": "The Godfather",
      "director": "Francis Ford Coppola",
      "year": 1972,
      "rating": 9.2,
      "categories": [
        "Crime",
        "Drama"
      ]
    },
    {
        "id": 2,
        "title": "The Shawshank Redemption",
        "director": "Frank Darabont",
        "year": 1994,
        "rating": 9.3,
        "categories": [
            "Crime",
            "Drama"
        ]
    },
    {
        "id": 3,
        "title": "The Hangover",
        "director": "Todd Phillips",
        "year": 2009,
        "rating": 7.7,
        "categories": [
            "Comedy"
        ]
    },
]

@app.get("/", tags=["root"])
def message():
    return HTMLResponse("<h1>Welcome to my movie API</h1>")


@app.get("/movies", tags=["movies"])
def get_movies():
    return movies

@app.get("/movies/{id}", tags=["movies"])
def get_movie(id: int):
    if id > len(movies):
        return None
    return movies[id-1]

@app.get("/movies/", tags=["movies"])
def get_movie_by_rating_and_year(rating: float, year: int):
    return [movie for movie in movies if movie["rating"] == rating and movie["year"] == year]

@app.get("/movies/category/{category}", tags=["movies"])
def get_movie_by_category(category: str):
    print("helo", category)
    return [movie for movie in movies if category in movie["categories"]]