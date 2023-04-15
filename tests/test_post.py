import pytest

from app.main import app
import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession



@pytest.mark.asyncio
async def test_post(Authorized_User):
    data={
         "title": "real",
    "content":"too real",
    "publish" : True
    }
    res = await Authorized_User.post("/post/", json= data)
    assert res.status_code == 201

@pytest.mark.asyncio
async def test_get_all_post(Authorized_User, post):
    res = await Authorized_User.get("/post/")
    assert res.status_code == 200

@pytest.mark.asyncio
async def test_get_all_post_with_no_post(Authorized_User):
    res = await Authorized_User.get("/post/")
    assert res.status_code == 204

@pytest.mark.parametrize("id, status_code", [(1,200), (2,404)])
@pytest.mark.asyncio
async def test_get_one_post(Authorized_User, post, id, status_code):
    res = await Authorized_User.get(f"/post/{id}")
    assert res.status_code == status_code

@pytest.mark.parametrize("id, status_code", [(1,204), (2,404)])
@pytest.mark.asyncio
async def test_delete_your_own_post(Authorized_User, post, id, status_code):
    res = await Authorized_User.delete(f"/post/{id}")
    assert res.status_code == status_code






@pytest.mark.parametrize("id, status_code", [(1,200), (2,404)])
@pytest.mark.asyncio
async def test_update_your_own_post(Authorized_User, post, id, status_code):

    data ={
        "title": "new era"
    }
    res = await Authorized_User.put(f"/post/{id}", json = data)
    assert res.status_code == status_code
    

