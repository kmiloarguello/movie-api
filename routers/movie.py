from fastapi import APIRouter,  Path, Query, Depends, status
from fastapi.responses import JSONResponse
from typing import  List, Optional
from pydantic import BaseModel, Field
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService

movie_router = APIRouter()

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

@movie_router.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(gt=0, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if result is None:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movie_by_rating_and_year(rating: float = Query(), year: int = Query()) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_rating_and_year(rating, year)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get("/movies/category/{category}", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movie_by_category(category: str) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post("/movies", tags=["movies"], status_code=201)
def add_movie(movie: Movie):
    db = Session() # create database session
    new_movie = MovieModel(**movie.model_dump()) # create new movie object
    db.add(new_movie) # add new movie to database
    db.commit() # save changes to database
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Movie created successfully"})

@movie_router.put("/movies/{id}", tags=["movies"], status_code=200)
def update_movie(id: int, movie: Movie):
    db = Session()
    existed_movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if existed_movie is None:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    existed_movie.title = movie.title
    existed_movie.director = movie.director
    existed_movie.year = movie.year
    existed_movie.rating = movie.rating
    existed_movie.categories = movie.categories
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Movie updated successfully"})

@movie_router.delete("/movies/{id}", tags=["movies"], status_code=200)
def delete_movie(id: int):
    db = Session()
    existed_movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if existed_movie is None:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    db.delete(existed_movie)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Movie deleted successfully"})

