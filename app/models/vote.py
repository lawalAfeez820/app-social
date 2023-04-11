from app.models.models import SQLModel
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from datetime import datetime
from pydantic import EmailStr
import sqlalchemy
from typing import List
from pydantic.types import conint


class Vote(SQLModel, table= True):
  
    post_id: int = Field(foreign_key = "posts.id", primary_key = True)
    user_id: int = Field(foreign_key = "user.id", primary_key = True)
    

class VoteDir(SQLModel):
    votedir: conint(le=1)