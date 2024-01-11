from fastapi import APIRouter,  Path, Query, Depends, status
from fastapi.responses import JSONResponse
from typing import  List, Optional
from pydantic import BaseModel, Field
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie as MovieSchema
movie_router = APIRouter()

@movie_router.get("/movies", tags=["movies"], response_model=List[MovieSchema], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[MovieSchema]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get("/movies/{id}", tags=["movies"], response_model=MovieSchema, status_code=200)
def get_movie(id: int = Path(gt=0, le=2000)) -> MovieSchema:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get("/movies/", tags=["movies"], response_model=List[MovieSchema], status_code=200)
def get_movie_by_rating_and_year(rating: float = Query(), year: int = Query()) -> List[MovieSchema]:
    db = Session()
    result = MovieService(db).get_movie_by_rating_and_year(rating, year)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get("/movies/category/{category}", tags=["movies"], response_model=List[MovieSchema], status_code=200)
def get_movie_by_category(category: str) -> List[MovieSchema]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post("/movies", tags=["movies"], status_code=201)
def add_movie(movie: MovieSchema):
    db = Session() # create database session
    new_movie = MovieService(db).add_movie(movie)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(new_movie))

@movie_router.put("/movies/{id}", tags=["movies"], status_code=200)
def update_movie(id: int, movie: MovieSchema):
    db = Session()
    existed_movie = MovieService(db).get_movie(id)
    if not existed_movie:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    result = MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.delete("/movies/{id}", tags=["movies"], status_code=200)
def delete_movie(id: int):
    db = Session()
    existed_movie = MovieService(db).get_movie(id)
    if not existed_movie:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "Movie deleted successfully"})

