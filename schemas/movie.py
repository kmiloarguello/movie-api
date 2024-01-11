
from typing import  Optional
from pydantic import BaseModel, Field

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
