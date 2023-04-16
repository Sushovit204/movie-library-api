from fastapi import FastAPI
from routers import movie, user, auth

app = FastAPI()

@app.get("/")
def welcome():
    return {"Welcome to my Music Library API.Use /docs endpoint to use all methods via swagger"}

app.include_router(movie.router)
app.include_router(user.router)
app.include_router(auth.router)