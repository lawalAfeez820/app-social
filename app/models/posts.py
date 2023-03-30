from app.models.models import SQLModel
from typing import Optional
from sqlmodel import Field
from datetime import datetime
import sqlalchemy

class Posts(SQLModel, table = True):
    id: Optional[int] = Field(primary_key = True, default = None)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    publish: bool 

class CreatePost(SQLModel):
    title: str
    content: str
    publish : bool = True

class PostOut(SQLModel):
    id: Optional[int] = Field(primary_key = True, default = None)
    title: str
    content: str
    publish : bool
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))\
    
