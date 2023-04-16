from schemas import Users
from fastapi import HTTPException, status, APIRouter
from database import mydb, mycursor
import utilis
import mysql.connector

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

#creating new users
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user:Users):
    try:
        #Hashing the password
        hashed_password = utilis.hash(user.password)
        user.password = hashed_password

        query = "INSERT INTO USERS(username, email, password) VALUES (%s,%s,%s)"
        val = (user.username, user.email, user.password)
        mycursor.execute(query, val)
        mydb.commit()
        return{"data":"User Created Successfully"}
    except mysql.connector.IntegrityError as e:
        #Throws error for duplicaiton of username
        if "username" in str (e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Username already taken")
        #Throws error if email already in use
        elif "email" in str (e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Email already in use")
    finally:
        mycursor.close()
        mydb.close()