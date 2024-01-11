from models.movie import Movie

class MovieService():

  def __init__(self, db) -> None:
    self.db = db

  def get_movies(self):
    return self.db.query(Movie).all()
  
  def get_movie(self, id: int):
    return self.db.query(Movie).filter(Movie.id == id).first()
  
  def get_movie_by_rating_and_year(self, rating: float, year: int):
    return self.db.query(Movie).filter(Movie.rating == rating, Movie.year == year).all()
  
  def get_movie_by_category(self, category: str):
    return self.db.query(Movie).filter(Movie.categories.contains(category)).all()