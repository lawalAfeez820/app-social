from app.models.models import SQLModel
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from datetime import datetime
from pydantic import EmailStr
import sqlalchemy

if TYPE_CHECKING:
    from app.models.users import User
    

class Posts(SQLModel, table = True):
    id: Optional[int] = Field(primary_key = True, default = None)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    publish: bool 
    owner_email: EmailStr = Field(foreign_key = "user.email")
    owner: Optional["User"] = Relationship(back_populates="posts", sa_relationship_kwargs={'lazy': 'selectin'})


class CreatePost(SQLModel):
    title: str
    content: str
    publish : bool = True
class FinalCreation(CreatePost):
    owner_email: EmailStr

class PostOwner(SQLModel):
    email: EmailStr
    user_name: str
    

class PostOut(SQLModel):
    id: Optional[int] = Field(primary_key = True, default = None)
    title: str
    content: str
    publish : bool
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    owner: PostOwner

   
    
class UpdatePost(SQLModel):
    title: Optional[str] = None
    content : Optional[str] = None
    publish: Optional[bool] = None
