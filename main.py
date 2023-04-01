from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from database import mydb, mycursor


app = FastAPI()

class Movie(BaseModel):
    title:str
    watched: bool = False

    @validator('title')
    def covert_lower_case(cls,v):
        return v.lower()

@app.get("/")
def welcome():
    return {"Welcome to my Music Library API.To view all the movies data go to /movies endpoint"}

#Gets a list of top movies
@app.get("/movies")
def get_movies_table():
    query = "SELECT title FROM MOVIES"
    mycursor.execute(query)
    rows = mycursor.fetchall()
    return{"movies":rows}

#Posting Favourite movie and save them to database
@app.post("/postmovies")
def create_favourite(new_movie: Movie):
    print(new_movie.dict())

    #Retriving tittle from Movies
    query = "SELECT title FROM MOVIES "
    mycursor.execute(query)
    exist_movie = exist_movie = [m[0] for m in mycursor.fetchall()]

    #Checking if the movie doesnot exist in the movie db
    if new_movie.title not in exist_movie:
        raise HTTPException(status_code=404, detail="Movie not found in Movies database")

    #Retriving tittle from FMovies
    query = "SELECT * FROM FMOVIE WHERE title = %s"
    val = (new_movie.title,)
    mycursor.execute(query, val)
    existing_movie = mycursor.fetchone()

    #Checking if the movie already exits 
    if existing_movie and existing_movie[2] == new_movie.watched:
        raise HTTPException(status_code=406, detail="Movie already exist in Favourite database")

    #Checking if existing movie has different watched status
    if existing_movie:
        query = "UPDATE FMOVIE SET watched =%s WHERE fid =%s"
        val = (new_movie.watched, existing_movie[0])
        mycursor.execute(query,val)
        mydb.commit()
        return {"data": new_movie}

    #If movie doesnot exist, inserting the data in MYsql DB
    query = "INSERT INTO FMOVIE (title, watched) VALUES (%s, %s)"
    val = (new_movie.title, new_movie.watched)
    mycursor.execute(query, val)
    mydb.commit()

    # Return a response 
    return{"data":new_movie}

#View favourite movies data
@app.get("/favmovies")
def favmovies():
    query = f"SELECT * FROM FMOVIE"
    mycursor.execute(query)
    rows = mycursor.fetchall()
    return{"favmovies":rows}
