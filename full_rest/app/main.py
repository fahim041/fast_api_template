from fastapi import FastAPI, status, Response, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from . import models
from .database import get_db
from .schema import Post, PostCreate

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

SessionDep = Annotated[Session, Depends(get_db)]


@app.get('/posts', response_model=dict[str, list[Post]])
def get_posts(db: SessionDep):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/{id}", response_model=dict[str, Post])
def get_post(id: int, db: SessionDep):
    post = db.query(models.Post).get(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"data": post}


@app.post("/posts", response_model=dict[str, Post], status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: SessionDep):
    post = models.Post(**post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)

    return {"data": post}


@app.put("/posts/{id}", response_model=dict[str, Post])
def update_post(id: int, post: PostCreate, db: SessionDep):
    post_to_update = db.query(models.Post).get(id)

    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    
    db.query(models.Post).filter(models.Post.id == id).update(post.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(post_to_update)

    return {"data": post_to_update}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: SessionDep):
    post_to_delete = db.query(models.Post).get(id)

    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    
    db.delete(post_to_delete)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)