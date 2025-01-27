from fastapi import HTTPException, status, Response, APIRouter
from ..database import SessionDep
from .. import models
from .. import schema
from ..utils import password

router = APIRouter(
    tags=['Users']
)

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_user(user: schema.UserCreate, db: SessionDep):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email: {user.email} already exists"
        )
    
    user.password = password.hash(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/users/{id}", response_model=schema.User)
def get_user(id: int, db: SessionDep):
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found"
        )
    return user