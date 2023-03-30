from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector


app = FastAPI()

#connecting to database
mydb = mysql.connector.connect(
    host ="localhost",
    user ="root",
    password = "Gaming.004",
    database = "imdb_movies"
)

#Creating cursor
mycursor = mydb.cursor()

class Movie(BaseModel):
    title:str
    watched: bool = False

@app.get("/")
def welcome():
    return {"Welcome to my Music Library API.To view all the movies data go to /movies endpoint"}

@app.get("/movies")
def get_movies_table():
    query = f"SELECT title FROM MOVIES"
    mycursor.execute(query)
    rows = mycursor.fetchall()
    return{"movies":rows}

@app.post("/postmovies")
def create_favourite(new_movie: Movie):
    print(new_movie.dict())

    #Inserting the data in MYsql DB
    sql = "INSERT INTO FMOVIE (title, watched) VALUES (%s, %s)"
    val = (new_movie.title, new_movie.watched)
    mycursor.execute(sql, val)
    mydb.commit()

    # Return a response 
    return{"data":new_movie}

