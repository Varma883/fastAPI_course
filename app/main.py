from enum import auto
from random import randrange
from typing import Optional, List # list is to for get All post in form of list
from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from sqlalchemy.orm import Session
from fastapi import Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas , utils
from .databse import engine, get_db
from .routers import post , user , auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='Tani@2056',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break   #  exits loop when success
    except Exception as error:
        print("Connecting to Database has failed")
        print("Error:", error)
        time.sleep(2)  # wait before retry


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
    
@app.get("/")
async def root():
    return {"message": "Welocome to my Api learnings"}



#uvicorn app.main:app --reload  