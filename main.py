from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"
app.description = "This is a very fancy movie API"

Base.metadata.create_all(bind=engine) # create tables in database

class JWTBearer(HTTPBearer):
    async def __call__(self, request : Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "ca@mi.lo":
            raise HTTPException(status_code=403, detail="Invalid credentials")
    
class User(BaseModel):
    email: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)

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

@app.get("/", tags=["root"], include_in_schema=False)
def message() -> dict:
    return HTMLResponse("<h1>Welcome to my movie API</h1>")

@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "ca@mi.lo" and user.password == "ca123":
        token = create_token(user.dict())
        return JSONResponse(status_code=200, content={"message": "Login successful", "token": token})
    return JSONResponse(status_code=401, content={"message": "Unauthorized"})

@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(gt=0, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if result is None:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movie_by_rating_and_year(rating: float = Query(), year: int = Query()) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.rating == rating, MovieModel.year == year).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get("/movies/category/{category}", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movie_by_category(category: str) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.categories.contains(category)).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.post("/movies", tags=["movies"], status_code=201)
def add_movie(movie: Movie):
    db = Session() # create database session
    new_movie = MovieModel(**movie.model_dump()) # create new movie object
    db.add(new_movie) # add new movie to database
    db.commit() # save changes to database
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Movie created successfully"})

@app.put("/movies/{id}", tags=["movies"], status_code=200)
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

@app.delete("/movies/{id}", tags=["movies"], status_code=200)
def delete_movie(id: int):
    db = Session()
    existed_movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if existed_movie is None:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    db.delete(existed_movie)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Movie deleted successfully"})

