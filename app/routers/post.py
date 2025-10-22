from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from ..databse import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional, List # list is to for get All post in form of list


router= APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#fetch all post
@router.get("/" , response_model= List[schemas.Post])
def get_posts(db: Session=Depends(get_db),
            user_id: int = Depends(oauth2.get_current_user) ):
    # cursor.execute("""SELECT * FROM posts """)
    # posts= cursor.fetchall()
    posts=db.query(models.Post).all()

    return posts


#Creating a New POST
@router.post("/", status_code=status.HTTP_201_CREATED , response_model=schemas.Post)
def create_post(post : schemas.PostBase, db: Session=Depends(get_db),
                 user_id: int = Depends(oauth2.get_current_user) ):
    # cursor.execute("""INSERT INTO posts (title , content , published) VALUES (%s, %s , %s) RETURNING * """,
    #                 (post.title, post.content, post.published))
    # new_post=cursor.fetchone()
    # conn.commit() # this line is actually going to push the changes into the databse
    print(user_id)
    new_post = models.Post(owner_id=int(user_id.id),**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#Fetch Post By ID
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int , db: Session=Depends(get_db),
             user_id: int= Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id == id).first()
   

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{id} is not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return{"message": f"Post with id:{id} is not found"}   
    return post


#Delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    if post.owner_id != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    post_query.delete(synchronize_session=False)
    db.commit()



#Update Post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostBase, db: Session=Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)
                ):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    if updated_post.owner_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Not authorized to perform requested action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

