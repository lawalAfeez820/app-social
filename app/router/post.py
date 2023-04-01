from fastapi import APIRouter, HTTPException,Depends
from fastapi.responses import Response
from sqlmodel import select, Session
from app.database.db import get_session
from app.models import posts
from typing import List



app = APIRouter(
        prefix = "/post", tags = ["POSTS"])

# post
@app.post("/", response_model = posts.PostOut, status_code = 201)
async def post(post_data: posts.CreatePost, db: Session = Depends(get_session)):

    # if not member logic 
    
    post_data = posts.Posts.from_orm(post_data)
    
    db.add(post_data)
    await db.commit()
    await db.refresh(post_data)
    return post_data

# get all post
@app.get("/", response_model = List[posts.PostOut])
async def get_all(db: Session = Depends(get_session)):
    
    data = await db.exec(select(posts.Posts))

    data: posts.Posts | None = data.all()
    if not data:
        raise HTTPException(status_code = 204, detail = "No post available yet")

    return data

# get post by id
@app.get("/{id}", response_model = posts.PostOut)
async def get_id(id: int, db: Session = Depends(get_session)):
    
    data = await db.exec(select(posts.Posts).where(posts.Posts.id == id))
    data: posts.Posts | None = data.first()
    if not data:
        raise HTTPException(status_code = 404, detail = f"No post with an id {id}")
    return data

#delete post
@app.delete("/{id}", status_code = 204)
async def delete_post(id: int, db: Session = Depends(get_session)):
    data: posts.Posts | None = await db.get(posts.Posts, id)
    if not data:
        raise HTTPException(status_code = 404, detail = f"No data with an id {id}")
    await db.delete(data)
    await db.commit()
    return Response(status_code = 204)

#update post
@app.put("/{id}")
async def update(id:int, post_data: posts.UpdatePost, db: Session= Depends(get_session)):
    
    data: posts.Posts | None = await db.get(posts.Posts, id)
    if not data:
        raise HTTPException(status_code = 404, detail = f"No data with an id {id}")
    post = post_data.dict(exclude_unset = True)
    
    for key, value in post.items():
        setattr(data, key, value)
        
        db.add(data)
        await db.commit()
        await db.refresh(data)
    return data





