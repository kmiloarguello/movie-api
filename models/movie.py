from config.database import Base
from sqlalchemy import Column, Integer, String, Float, PickleType

class Movie(Base):
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String(255))
  year = Column(Integer)
  rating = Column(Float)
  categories = Column(PickleType)
