from sqlmodel import SQLModel, Field
from typing import Optional

class Test(SQLModel, table = True):
    id: Optional[int] = Field(primary_key = True, default = None)