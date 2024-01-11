from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"
app.description = "This is a very fancy movie API"

class Movie(BaseModel):
    id: Optional[int] = Field(None, title="The ID of the movie", gt=0)
    title: str = Field(min_length=1, max_length=50)
    director: str = Field(min_length=1, max_length=50)
    year: int = Field(ge=1900, le=2100)
    rating: float = Field(ge=0.0, le=10.0)
    categories: list

    class Config:
      json_schema_extra = {
          "example": {
              "id": 1,
              "title": "The Godfather",
              "director": "Francis Ford Coppola",
              "year": 1972,
              "rating": 9.2,
              "categories": ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Thriller"]
          }
      }

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
def get_movie(id: int = Path(gt=0, le=2000)):
    if id > len(movies):
        return None
    return movies[id-1]

@app.get("/movies/", tags=["movies"])
def get_movie_by_rating_and_year(rating: float = Query(max_length=5), year: int = Query(min_length=4,max_length=4)):
    return [movie for movie in movies if movie["rating"] == rating and movie["year"] == year]

@app.get("/movies/category/{category}", tags=["movies"])
def get_movie_by_category(category: str):
    print("helo", category)
    return [movie for movie in movies if category in movie["categories"]]

@app.post("/movies", tags=["movies"])
def add_movie(movie: Movie):
    movies.append({
        "id": movie.id,
        "title": movie.title,
        "director": movie.director,
        "year": movie.year,
        "rating": movie.rating,
        "categories": movie.categories
    })
    return movies[-1]

@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    if id > len(movies):
        return None
    movies.pop(id-1)
    return movies

@app.put("/movies/{id}", tags=["movies"])
def update_movie(id: int, movie: Movie):
    movies[id-1] = {
        "title": movie.title,
        "director": movie.director,
        "year": movie.year,
        "rating": movie.rating,
        "categories": movie.categories
    }
    return movies[id-1]