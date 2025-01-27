from fastapi import APIRouter, HTTPException, status, Depends
from ..database import SessionDep
from .. import models
from .. import schema
from ..utils import password, jwt

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schema.AccessToken)
def login(user_credentails: schema.UserLogin, db: SessionDep):
    user = db.query(models.User).filter(models.User.email == user_credentails.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    
    verify = password.verify(user_credentails.password, user.password)

    if not verify:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentails"
        )
    
    return {"token": jwt.create_access_token(data={"id": user.id, "email": user.email}), "token_type": "Bearer"}

@router.get("/profile")
def get_profile(current_user: schema.UserTokenData = Depends(jwt.get_current_user)):
    return {"id": current_user.id, "email": current_user.email}