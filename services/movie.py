from models.movie import Movie as MovieModel
from schemas.movie import Movie as MovieSchema

class MovieService():
  def __init__(self, db) -> None:
    self.db = db

  def get_movies(self):
    return self.db.query(MovieModel).all()
  
  def get_movie(self, id: int):
    return self.db.query(MovieModel).filter(MovieModel.id == id).first()
  
  def get_movie_by_rating_and_year(self, rating: float, year: int):
    return self.db.query(MovieModel).filter(MovieModel.rating == rating, MovieModel.year == year).all()
  
  def get_movie_by_category(self, category: str):
    return self.db.query(MovieModel).filter(MovieModel.categories.contains(category)).all()
  
  def add_movie(self, movie: MovieSchema):
    new_movie = MovieModel(**movie.model_dump())
    self.db.add(new_movie)
    self.db.commit()
    return new_movie
  
  def update_movie(self, id: int, data: MovieSchema):
    movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
    movie.title = data.title
    movie.director = data.director
    movie.year = data.year
    movie.rating = data.rating
    movie.categories = data.categories
    self.db.commit()
    return movie
  
  def delete_movie(self, id: int):
    movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
    self.db.delete(movie)
    self.db.commit()
    return