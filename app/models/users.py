from app.models.models import SQLModel

from sqlmodel import Field, Relationship
from typing import Optional,List, TYPE_CHECKING
from pydantic import EmailStr
import sqlalchemy
from datetime import datetime
from typing import Optional

if TYPE_CHECKING:
    from app.models.posts import Posts
    from app.models.comments import Comment

class User(SQLModel, table= True):
    id: Optional[int] = Field(primary_key = True, default = None)
    email: EmailStr = Field(unique = True)
    user_name: Optional[str] = None
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    posts: Optional["Posts"] = Relationship(back_populates="owner", sa_relationship_kwargs={'lazy': 'selectin'})
    comments: "Comment" = Relationship(back_populates="users", sa_relationship_kwargs={'lazy': 'selectin'})
   

class CreateUser(SQLModel):
    email: EmailStr
    password: str
    confirm_password: str
    user_name: str
class UserOut(SQLModel):
    id: int
    email: EmailStr
    user_name: str
    created_at: datetime
    updated_at: datetime

class UserPost(SQLModel):

    id: int
    title: str
    content: str
    publish : bool
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))

class UserData(UserOut):
    posts: List[UserPost]

class LoginCred(SQLModel):
    access_token: str
    token_type: str

class PasswordData(SQLModel):
    old_password: str
    new_password: str
    confirm_newpassword: str

class PlainText(SQLModel):
    detail: str

class ForgetPassword(SQLModel):
    email: EmailStr