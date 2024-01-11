# Movie API

## Description

This is a simple API that allows you to create, read, update and delete movies from a database.

## Installation and Usage

1. Clone the repository.
2. Get the required dependencies in the `requirements.txt` file with `pip install -r requirements.txt`.
3. Run the app with Uvicorn
   
```
uvicorn main:app --reload --port 8000 --host 0.0.0.0
```

## Endpoints

### GET /movies

Returns a list of all movies in the database.

### GET /movies/{id}

Returns a movie with the given id.

### GET /movies/

Returns a list of movies with the given rating and year.

### GET /movies/categories/{category}

Returns a list of movies with the given category.

### POST /movies

Creates a new movie in the database.

### PUT /movies/{id}

Updates a movie with the given id.

### DELETE /movies/{id}

Deletes a movie with the given id.

## Database

The database used is SQLite. The database file is `my-movie-api.db.sqlite`.


### Aknowledgements

This project was made with the help of the [FastAPI documentation](https://fastapi.tiangolo.com/). Following the course at Platzi, [Curso de API REST con FastAPI](https://platzi.com/clases/fastapi/).




