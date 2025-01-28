from fastapi import HTTPException, status, Response, APIRouter, Depends
from ..database import SessionDep
from .. import models
from .. import schema
from ..utils import jwt

router = APIRouter(
    tags=['Posts']
)

@router.get('/posts', response_model=list[schema.Post])
def get_posts(db: SessionDep, limit: int = 2):
    print("limit", limit)
    posts = db.query(models.Post).limit(limit).all()
    return posts


@router.get("/posts/{id}", response_model=schema.Post)
def get_post(id: int, db: SessionDep, current_user: schema.UserTokenData = Depends(jwt.get_current_user)):
    post = db.query(models.Post).get(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found"
        )
    return post


@router.post("/posts", response_model=schema.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schema.PostCreate, db: SessionDep, current_user: schema.UserTokenData = Depends(jwt.get_current_user)):
    post = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.put("/posts/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate, db: SessionDep, current_user: schema.UserTokenData = Depends(jwt.get_current_user)):
    post_to_update = db.query(models.Post).get(id)

    if not post_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found"
        )
    
    if post_to_update.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    db.query(models.Post).filter(models.Post.id == id).update(post.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(post_to_update)

    return post_to_update


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: SessionDep, current_user: schema.UserTokenData = Depends(jwt.get_current_user)):
    post_to_delete = db.query(models.Post).get(id)

    if not post_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found"
        )
    
    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    db.delete(post_to_delete)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)