from app.models import comments, users, posts

from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import select, Session, desc
from app.database.db import get_session
from app.OAuth.oauth import Token_Data
from app.models.comments import Comment, FinalComment, MakeComment, CommentOut
from app.models.posts import Posts
from typing import List
from sqlalchemy.engine.result import ScalarResult

app = APIRouter(tags=["Comments"],
prefix = "/comment")




@app.post("/{post_id}", response_model = List[CommentOut])
async def make_comment(post_id: int, comment: MakeComment, user: users.User= Depends(Token_Data.get_current_user), db: Session= Depends(get_session)):
    post:Posts| None = await db.get(Posts, post_id)
    if not post:
        raise HTTPException(404, detail = f"No post with id {post_id}")
    comment = {**comment.dict(), "post_id": post_id, "user_id": user.id}
    comment = FinalComment(**comment)
    comment = Comment.from_orm(comment)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    comments: ScalarResult = await db.exec(select(Comment).where(Comment.post_id == post_id).order_by(desc(Comment.updated_at)))
    print(type((comments)))
    comments = comments.all()
    return comments

@app.delete("/{comment_id}", response_model = List[CommentOut])
async def delete_comment(comment_id:int, user: users.User= Depends(Token_Data.get_current_user), db: Session= Depends(get_session)):



    comment: Comment | None = await db.get(Comment, comment_id)

    if not comment:
        raise HTTPException(404, detail = f"No comment with id {comment_id}")
    if comment.user_id != user.id:
        raise HTTPException(409, detail= "You can't delete post that is not yours")
    post_id = comment.post_id
    await db.delete(comment)
    await db.commit()
    comments = await db.exec(select(Comment).where(Comment.post_id == post_id).order_by(desc(Comment.updated_at)))
    
    comments = comments.all()
    return comments

@app.get("/{post_id}", response_model = users.PlainText)
async def count_comment(post_id: int, db: Session= Depends(get_session), user: users.User= Depends(Token_Data.get_current_user)):
    post: Posts | None = await db.get(Posts, id)
    if not post:
        raise HTTPException(404, detail= f"No post with id {post_id}")
    length = len(post.comments)
    if length == 0:
        return users.PlainText(detail = "There is no comment for this post")
    return users.PlainText(detail = f"There is/are {length} comment(s) for this post")

    