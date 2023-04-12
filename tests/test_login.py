import pytest

from app.main import app
import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.parametrize("email, password, status_code", [
    ("lawalafeez820@gmail.com", "test", 200),
    ("lawal", "test", 409),
    ("lawalafeez820@gmail.com", "tes", 409)
])
@pytest.mark.asyncio
async def test_login(user1, async_client, password, email, status_code):

    data = {"username":email, "password" : password}
    res = await async_client.post("/login", data = data)

    res.status_code == status_code


@pytest.mark.parametrize("email, status_code", [("lawalafeez820@gmail.com", 200), ("lawa@gmail.com", 409)])
@pytest.mark.asyncio
async def test_forget_password(user1, async_client, email, status_code):
    data ={
        "email": email
    }
    res = await async_client.post("/forgetpassword", json = data)
    assert res.status_code == status_code

