from fastapi import APIRouter, HTTPException, status
import schemas, utilis, oauth2
from database import mycursor

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(user_credential:schemas.UserLogin):
    query = f"SELECT * FROM users WHERE username ='{user_credential.username}'"
    mycursor.execute(query)
    user_name= mycursor.fetchone()
    if mycursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Username.")
    if not utilis.verify(user_credential.password, user_name[3]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Password.")
    
    access_token = oauth2.create_access_token(data={"user":user_name[0]})
    
    return{"access_token":access_token}