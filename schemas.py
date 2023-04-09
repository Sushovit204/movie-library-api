from pydantic import BaseModel, validator, EmailStr, constr
from typing import Optional

class Movies(BaseModel):
    title:str
    watched: bool = False

    @validator('title')
    def covert_lower_case(cls,v):
        return v.lower()
    

class Users(BaseModel):
    #username accepting string without spaces
    username : constr(strict=True,regex=r'^\S+$',)

    @validator('username')
    def convert_lower(cls,v):
        return v.lower()
    
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None


