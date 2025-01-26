from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class config:
        orm_mode = True


class PostCreate(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False