from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from sqlalchemy.orm import Session
from fastapi import Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import models
from .databse import engine, get_db




models.Base.metadata.create_all(bind=engine)

app = FastAPI()




class Post(BaseModel):
    title: str
    content: str
    published: bool=True



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
        break   # ✅ exits loop when success
    except Exception as error:
        print("Connecting to Database has failed")
        print("Error:", error)
        time.sleep(2)  # wait before retry


    

my_post = [{"title":"Title of post 1", "content":"i love piszza", "id":1},
           {"title":"Title of post 2", "content":"Beaches Love me", "id":2}]


def find_post(id): #Returns the matching post
    for p in my_post:
        if p["id"] == id:   # int vs int comparison
            return p

#You’d use enumerate() when you also need the index of the item—like 
#when you want to delete it from a list using pop(index):        
def find_delete_post(id): 
    for index, post in enumerate(my_post):
        if post["id"] == id:
            return my_post.pop(index)



@app.get("/")
async def root():
    return {"message": "Welocome to my Api learnings"}


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts= db.query(models.Post).all()
  
    return {"data": posts}


#fetch all post
@app.get("/posts")
def get_posts(db: Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts= cursor.fetchall()
    posts=db.query(models.Post).all()

    return{"data":posts}


#Creating a New POST
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post : Post, db: Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title , content , published) VALUES (%s, %s , %s) RETURNING * """,
    #                 (post.title, post.content, post.published))
    # new_post=cursor.fetchone()
    # conn.commit() # this line is actually going to push the changes into the databse
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return{"data": new_post} 

#Fetch Post By ID
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s """ , (str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{id} is not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return{"message": f"Post with id:{id} is not found"}   
    return{"post_detail": post}



#delete post
@app.delete("/posts/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int):
    cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING * """, (str(id)))
    post=cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{id} is not found")
    
    return{"message": f"post with id:{id} is prminatly deleted"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
        cursor.execute(
            """
            UPDATE posts 
            SET title = %s, content = %s, published = %s
            WHERE id = %s
            RETURNING *
            """,
            (post.title, post.content, post.published, str(id))
        )
        updated_post = cursor.fetchone()
        conn.commit()

        if not updated_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {id} not found"
            )

        return {"post_detail": updated_post}
