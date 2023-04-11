from fastapi import APIRouter, HTTPException,Depends
from fastapi.responses import Response
from sqlmodel import select, Session
from app.database.db import get_session
from app.models import posts, users
from typing import List
from app.OAuth.oauth import Token_Data
from sqlalchemy.engine.result import ScalarResult



app = APIRouter(
        prefix = "/post", tags = ["POSTS"])

# post
@app.post("/", response_model = posts.PostOut, status_code = 201)
async def post(post_data: posts.CreatePost, db: Session = Depends(get_session), user: users.User= Depends(Token_Data.get_current_user)):

    # if not member logic 
    
    temp_data = post_data.dict()
    temp_data={**temp_data, "owner_email":user.email}
   
    post_data = posts.FinalCreation(**temp_data)
   
    post_data = posts.Posts.from_orm(post_data)
    
    
    db.add(post_data)
    await db.commit()
    await db.refresh(post_data)
    return post_data

# get all post
@app.get("/", response_model = List[posts.PostOut])
async def get_all(db: Session = Depends(get_session), user: users.User = Depends(Token_Data.get_current_user)):
    
    data: ScalarResult = await db.exec(select(posts.Posts))

    data: posts.Posts | None = data.all()
    if not data:
        raise HTTPException(status_code = 204, detail = "No post available yet")

    return data


# get post by id
@app.get("/{post_id}", response_model = posts.PostOut)
async def get_id(post_id: int, db: Session = Depends(get_session), user: users.User = Depends(Token_Data.get_current_user)):
    
    data: ScalarResult= await db.exec(select(posts.Posts).where(posts.Posts.id == post_id))
    data: posts.Posts | None = data.first()
    if not data:
        raise HTTPException(status_code = 404, detail = f"No post with an id {post_id}")
    return data

#delete post
@app.delete("/{post_id}", status_code = 204)
async def delete_post(post_id: int, db: Session = Depends(get_session), user: users.User = Depends(Token_Data.get_current_user)):
    
    data: posts.Posts | None = await db.get(posts.Posts, post_id)
    if not data:
        raise HTTPException(status_code = 404, detail = f"No data with an id {post_id}")
    if user.email != data.owner_email:
        raise HTTPException(status_code=403, detail ="You are not the creator of this post")
    await db.delete(data)
    await db.commit()
    return Response(status_code = 204)

#update post
@app.put("/{post_id}", response_model = posts.PostOut)
async def update(post_id:int, post_data: posts.UpdatePost, db: Session= Depends(get_session), user: users.User = Depends(Token_Data.get_current_user)):

    data: posts.Posts | None = await db.get(posts.Posts, post_id)
    if not data:
        raise HTTPException(status_code = 404, detail = f"No data with an id {post_id}")
    if user.email != data.owner_email:
        raise HTTPException(status_code=403, detail ="You are not the creator of this post")
    post: dict = post_data.dict(exclude_unset = True)
    
    for key, value in post.items():
        setattr(data, key, value)
        
        db.add(data)
        await db.commit()
        await db.refresh(data)
    return data





