from fastapi import FastAPI

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"
app.description = "This is a very fancy movie API"

@app.get("/", tags=["Root"])
def message():
    return {"message": "Hello World"}