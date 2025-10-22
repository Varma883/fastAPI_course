from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from ..databse import  get_db
from sqlalchemy.orm import Session
from fastapi import Depends
#This is a dependency class to collect the username and password as form data for an OAuth2 password flow.
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 




router =APIRouter(
    tags=['Authentication']
)


router = APIRouter(tags=["Authentication"])

@router.post('/login', response_model=schemas.Token)      
def login(user_credentials: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):
    #  Find the user by email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    return {
        "user_id": user.id,
        "access_token": access_token, 
        "token_type":"bearer"}


    
   
   
    