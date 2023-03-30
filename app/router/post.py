from fastapi import APIRouter, HTTPException,Depends
from sqlmodel import select, Session
from app.database.db import get_session
from app.models import posts


app = APIRouter(
        prefix = "/post", tags = ["POSTS"])


@app.post("/", response_model = posts.PostOut, status_code = 201)
async def post(post_data: posts.CreatePost, db: Session = Depends(get_session)):

    # if not member logic 
    
    post_data = posts.Posts.from_orm(post_data)
    
    db.add(post_data)
    await db.commit()
    await db.refresh(post_data)
    return post_data



