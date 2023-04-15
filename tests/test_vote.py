import pytest

from app.main import app
import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.parametrize("id, votedir, status_code", [
    (2, 1, 404),
    (1, 0, 409)
     
])
@pytest.mark.asyncio
async def test_like1(Authorized_User, post, id, votedir, status_code):

    data = {
        "votedir": votedir
    }

    res = await Authorized_User.post(f"/like/{id}", json = data)

    assert res.status_code == status_code








@pytest.mark.parametrize("id, votedir, detail", [
    
    (1, 0, f"You can't like/unlike the post created by you")
     
])
@pytest.mark.asyncio
async def test_like_my_post(Authorized_User,post, id, votedir, detail):

    data = {
        "votedir": votedir
    }

    res = await Authorized_User.post(f"/like/{id}", json = data)

    assert res.json()["detail"]== detail