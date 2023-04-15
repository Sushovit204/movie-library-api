from jose import JWTError, jwt
import schemas, os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

#Loading ennvironment variables from .env
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

#Acessing the variables
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTE = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTE')
ALGORITHM = os.getenv('ALGORITHM')

def create_access_token(data:dict):
    to_encoded = data.copy()

    expire  = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encoded.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encoded, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id:str = payload.get("user_id")

        if id is None:
            raise credential_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not validate credential",
                                         headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credential_exception)

