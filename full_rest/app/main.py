from fastapi import FastAPI

from app import models
from .database import engine
from .routers import user, post, auth


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"status": "up"}

