from fastapi import APIRouter, HTTPException, status, Depends
import utilis, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import mycursor

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(user_credential:OAuth2PasswordRequestForm = Depends()):
    query = f"SELECT * FROM users WHERE username ='{user_credential.username}'"
    mycursor.execute(query)
    user_name= mycursor.fetchone()
    if mycursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Username.")
    if not utilis.verify(user_credential.password, user_name[3]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Password.")
    
    access_token = oauth2.create_access_token(data={"user_id":user_name[0]})
    
    return{"access_token":access_token, "token_type":"bearer"}