
import pytest

from app.main import app
import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.parametrize("id, status_code", [(1,201), (2,404)])
@pytest.mark.asyncio
async def test_comment(Authorized_User, post, id, status_code):
    data={
      "comment": "commenting"
    }
    res = await Authorized_User.post(f"/comment/{id}", json= data)
    assert res.status_code == status_code


@pytest.mark.parametrize("id, status_code", [(1,200), (2,404)])
@pytest.mark.asyncio
async def test_delete_yourown_comment(Authorized_User, post, id, status_code, comment):
    
    res = await Authorized_User.delete(f"/comment/{id}")
    assert res.status_code == status_code


@pytest.mark.parametrize("id, status_code", [(1,200), (2,404)])
@pytest.mark.asyncio
async def test_count_comment(Authorized_User, id, status_code, comment):
    
    res = await Authorized_User.get(f"/comment/{id}")
    assert res.status_code == status_code

