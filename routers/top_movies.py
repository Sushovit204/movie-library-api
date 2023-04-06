from fastapi import status, APIRouter
from database import mycursor

router= APIRouter(
    prefix="/movies"
)

#Gets a list of top movies
@router.get("/", status_code=status.HTTP_200_OK)
def get_movies_table():
    query = "SELECT title FROM MOVIES"
    mycursor.execute(query)
    rows = mycursor.fetchall()
    return{"movies":rows}