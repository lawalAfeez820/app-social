from fastapi import APIRouter, HTTPException,Depends
from fastapi.responses import Response
from sqlmodel import select, Session
from app.database.db import get_session
from app.models import posts, users, vote
from typing import List
from app.OAuth.oauth import Token_Data
from sqlalchemy.engine.result import ScalarResult




app = APIRouter(
        prefix = "/like", tags = ["VOTES"])

@app.post("/{post_id}", status_code = 201)
async def like(post_id: int, votes: vote.VoteDir, user:users.User = Depends(Token_Data.get_current_user), db: Session = Depends(get_session)):

    post: posts.Posts| None = await db.get(posts.Posts, post_id)
    
    if not post:
        raise HTTPException(404, detail = f"No post of id {post_id}")

    if post.owner_email == user.email and (votes.votedir == 1 or votes.votedir == 0):
        raise HTTPException(409, detail = f"You can't like/unlike the post created by you")
    
    vote_already: ScalarResult = await db.exec(select(vote.Vote).where(vote.Vote.post_id == post_id).where(vote.Vote.user_id == user.id))
    vote_already: vote.Vote |None = vote_already.first()

    if vote_already and votes.votedir == 1:
        raise HTTPException(409, detail = f"You can't like the post you already liked before")
    
    if vote_already and votes.votedir == 0:
        await db.delete(vote_already)
        await db.commit()
        return Response(status_code= 204)

    if not vote_already and votes.votedir == 0:
        raise HTTPException(409, detail = f"You can't dislike the post that has not been liked by you before")
        

    if votes.votedir == 1:
        data = vote.Vote(post_id = post_id, user_id = user.id)
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return users.PlainText(detail= f"Post likes successfully")
    
@app.get("/count", response_model = users.PlainText)
async def count_vote(post_id:int, user:users.User = Depends(Token_Data.get_current_user), db: Session = Depends(get_session)):
    votes: ScalarResult  = await db.exec(select(vote.Vote).where(vote.Vote.post_id == post_id))
    votes: vote.Vote | None = votes.all()
    if not vote:
        raise HTTPException(404, detail = f"No like for post of id {post_id}")
    return users.PlainText(detail = f"The total number of like for post of id {post_id} is {len(votes)}")

