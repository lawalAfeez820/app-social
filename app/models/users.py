from app.models.models import SQLModel

from sqlmodel import Field, Relationship
from typing import Optional,List, TYPE_CHECKING
from pydantic import EmailStr
import sqlalchemy
from datetime import datetime

if TYPE_CHECKING:
    from app.models.posts import Posts

class User(SQLModel, table= True):
    id: Optional[int] = Field(primary_key = True, default = None)
    email: EmailStr = Field(unique = True)
    user_name: Optional[str] = None
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    posts: Optional["Posts"] = Relationship(back_populates="owner")

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

class LoginCred(SQLModel):
    access_token: str
    token_type: str