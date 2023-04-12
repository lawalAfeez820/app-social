import pytest

from app.main import app
import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.parametrize("email, password, status_code", [
    ("lawalafeez820@gmail.com", "test, 200"),
    ("lawal", "test, 409"),
    ("lawalafeez820@gmail.com", "tes, 409")
])
@pytest.mark.asyncio
async def login(user1, async_client, password, email, status_code):

    data = {"username":email, "password" : password}
    res = async_client.post("/login", data = data)

    res.status_code == status_code
