from schemas import Movies, UpdateFmovie
from fastapi import HTTPException, status, APIRouter, Depends
from database import mydb, mycursor
import oauth2

router = APIRouter(
    prefix="/fmovies",
    tags=["Favourite Movies"]
)

#Posting Favourite movie and save them to database
@router.post("/",status_code=status.HTTP_201_CREATED)
def create_favourite(new_movie: Movies, user_id : int = Depends(oauth2.get_current_user)):

    #Retriving tittle from Movies
    query = "SELECT title FROM MOVIES "
    mycursor.execute(query)
    exist_movie = [m[0] for m in mycursor.fetchall()]

    #Checking if the movie doesnot exist in the movie db
    if new_movie.title not in exist_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found in Movies database")

    #Retriving tittle from FMovies of uid
    query= f"SELECT * FROM FMOVIES WHERE title = '{new_movie.title}' AND uid = {user_id.id}"
    mycursor.execute(query)
    existing_movie = mycursor.fetchone()

    #Checking if the movie already exits 
    if existing_movie is None:
        #If movie doesnot exist, inserting the data in MYsql DB
        query = "INSERT INTO FMOVIES (title, watched, uid) VALUES (%s, %s, %s)"
        val = (new_movie.title, new_movie.watched, user_id.id )
        mycursor.execute(query, val)
        mydb.commit()

         # Return a response 
        return{"title": new_movie.title, "watched": new_movie.watched}
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                            detail="Movie already exist in Favourite database")

#View favourite movies data
@router.get("/", status_code=status.HTTP_200_OK)
def favmovies():
    query = f"SELECT * FROM FMOVIES"
    mycursor.execute(query)
    rows = mycursor.fetchall()
    return{"favmovies":rows}

#deleting favourite movies
@router.delete("/{id}")
def delete_favmovie(id:int, user_id : int = Depends(oauth2.get_current_user)):
    query = f"SELECT uid FROM FMOVIES WHERE fid = {id}"
    mycursor.execute(query)
    result = mycursor.fetchone()
    if result is not None:
        uid = result[0]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Favourite movie of ID {id} doesnot exist in your database ")

    if int(uid) != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Favourite movie of ID {id} does not belong to uid {user_id.id}") 

    dquery=f"DELETE FROM FMOVIES WHERE fid= {id}"
    mycursor.execute(dquery)
    mydb.commit()
    return {"message":f"Favourite movie of ID {id} was deleted"}

#Updating the fmovie 
@router.put("/{id}")
def update_favmovie(id: int, new_movie: UpdateFmovie, user_id: int = Depends(oauth2.get_current_user)):
    # retrieve the Favourite movie
    query = f"SELECT uid, watched FROM FMOVIES WHERE fid = {id}"
    mycursor.execute(query)
    existing_movie = mycursor.fetchone()

    # check if Favourite movie exists
    if existing_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Favourite movie of ID {id} does not exist in your database")

    # check if the Favourite movie belongs to the user
    if int(existing_movie[0]) != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Favourite movie of ID {id} does not belong to uid {user_id.id}")


    # update the watched status of the Favourite movie
    query = "UPDATE FMOVIES SET watched = %s WHERE fid = %s"
    val = (new_movie.watched, id)
    mycursor.execute(query, val)
    mydb.commit()

    return {"message": f"Favourite movie of ID {id} was updated"}