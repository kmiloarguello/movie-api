from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import ErrorHandlerMiddleware
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"
app.description = "This is a very fancy movie API"

app.add_middleware(ErrorHandlerMiddleware) # add error handler middleware

# Register routers
app.include_router(user_router)
app.include_router(movie_router)

Base.metadata.create_all(bind=engine) # create tables in database

