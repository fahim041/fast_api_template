import os
from fastapi import FastAPI, status, Response, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()

try:
    conn = psycopg2.connect(host='localhost', database='fast_api', user='root',
                            password='root', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('Database connected!')
except Exception as error:
    print('Error connecting database', error)
    os._exit(1)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get('/posts')
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute(
        """
            INSERT INTO posts (title, content, published) VALUES
            (%s, %s, %s) RETURNING *
        """, (post.title, post.content, post.published)
    )

    post = cursor.fetchone()
    conn.commit()
    return {"data": post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """
            UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
        """, (post.title, post.content, post.published, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"data": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s return *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)