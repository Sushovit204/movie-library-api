from fastapi import FastAPI, Response
from pydantic import BaseModel
import mysql.connector
import json 

app = FastAPI()

#connecting to database
db = mysql.connector.connect(
    host ="localhost",
    user ="root",
    password = "Gaming.004",
    database = "imdb_movies"
)


# class Movie(BaseModel):
#     title:str
#     watched: bool = False

@app.get("/")
def welcome():
    return {"Welcome to my Music Library API.To view all the movies data go to /movies endpoint"}

@app.get("/movies")
def get_movies_table(response:Response):
    cursor = db.cursor()
    query = f"SELECT title FROM MOVIES"
    cursor.execute(query)
    rows = cursor.fetchall()
    return{"movies":rows}

# @app.get("/post")
# def creating_favourite(new_movie = Movie)
