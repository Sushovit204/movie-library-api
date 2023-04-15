from schemas import Movies
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
        raise HTTPException(status_code=404, detail="Movie not found in Movies database")

    #Retriving tittle from FMovies
    query = "SELECT * FROM FMOVIES WHERE title = %s"
    val = (new_movie.title,)
    mycursor.execute(query, val)
    existing_movie = mycursor.fetchone()

    #Checking if the movie already exits 
    if existing_movie and existing_movie[2] == new_movie.watched:
        raise HTTPException(status_code=406, detail="Movie already exist in Favourite database")

    #Checking if existing movie has different watched status
    if existing_movie:
        query = "UPDATE FMOVIES SET watched =%s WHERE fid =%s"
        val = (new_movie.watched, existing_movie[0])
        mycursor.execute(query,val)
        mydb.commit()
        return {"data": new_movie}

    #If movie doesnot exist, inserting the data in MYsql DB
    query = "INSERT INTO FMOVIES (title, watched, uid) VALUES (%s, %s, %s)"
    val = (new_movie.title, new_movie.watched, user_id.id )
    mycursor.execute(query, val)
    mydb.commit()

    # Return a response 
    return{"title": new_movie.title, "watched": new_movie.watched}

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
    # return(f"uid: {uid}, user_id.id: {user_id.id}")
    if int(uid) != int(user_id.id):
         return {"message": f"Favourite movie of ID {id} does not belong to uid {user_id.id}"}

    dquery=f"DELETE FROM FMOVIES WHERE fid= {id}"
    mycursor.execute(dquery)
    mydb.commit()
    return {"message":f"Favourite movie of ID {id} was deleted"}
       
