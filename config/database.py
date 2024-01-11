import os
from sqlalchemy import create_engine # database connection
from sqlalchemy.orm.session import sessionmaker # session manipulation
from sqlalchemy.ext.declarative import declarative_base # table manipulation

sqlite_file_name = 'my-movie-api.db.sqlite'
base_dir = os.path.abspath(os.path.dirname(__file__))

sqlite_uri = 'sqlite:///' + os.path.join(base_dir, sqlite_file_name)
engine = create_engine(sqlite_uri, echo=True)
session = sessionmaker(bind=engine)()
Base = declarative_base()