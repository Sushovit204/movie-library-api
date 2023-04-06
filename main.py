from fastapi import FastAPI, HTTPException, status
from routers import movie, user

app = FastAPI()

@app.get("/")
def welcome():
    return {"Welcome to my Music Library API.Use /docs endpoint to use all methods via swagger"}

app.include_router(movie.router)
app.include_router(user.router)


    
