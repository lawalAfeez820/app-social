from app.models.models import SQLModel
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from datetime import datetime
from pydantic import EmailStr
import sqlalchemy
from typing import List


if TYPE_CHECKING:
    from app.models.users import User,  UserPost

    from app.models.posts import Posts, PostOwner
    
    
class Comment(SQLModel, table= True):
    id: Optional[int] = Field(default = None, primary_key = True)
    post_id: int = Field(foreign_key ="posts.id", nullable = True)
    user_id: int = Field(foreign_key ="user.id")
    comment: str

    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    
    post: "Posts" = Relationship(back_populates="comments", sa_relationship_kwargs={'lazy': 'selectin'})
    users: "User" = Relationship(back_populates="comments", sa_relationship_kwargs={'lazy': 'selectin'})


class MakeComment(SQLModel):
    comment: str

class FinalComment(MakeComment):
    post_id:  int
    user_id: int


  
class CommentOut(SQLModel):
    comment: str
    created_at: datetime
    updated_at: datetime
    users: "PostOwner"
    post: "UserPost"




   