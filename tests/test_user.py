import pytest

from app.main import app
import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.parametrize("email, password, confirm_password, user_name, status_code",
    [("adekunle@gmail.com", "123", "123", "law", 201),
    ("adekunle@gmail.com", "123", "12", "law", 403),
    ("lawalafeez820@gmail.com", "123", "123", "lawa", 409),
    ("adekunle@gmail.com", "123", "123", "lawal", 409)])
@pytest.mark.asyncio
async def test_create_user(user1, email, password, confirm_password,   
                            user_name, status_code, async_client: AsyncClient):
    
    data = {"email": email,
        "password":password,
        "confirm_password":confirm_password,
        "user_name": user_name
        

    }
    
    res = await async_client.post("/user/", json = data)
    
    assert res.status_code == status_code


@pytest.mark.asyncio
async def test_user_all_with_auth(Authorized_User: AsyncClient):

    res = await Authorized_User.get("/user/all")
    assert res.status_code == 200

@pytest.mark.asyncio
async def test_user_all_without_auth(async_client: AsyncClient):

    res = await async_client.get("/user/all")
    assert res.status_code == 401


@pytest.mark.parametrize("old_password, new_password, confirm_newpassword, status_code",
        [ ("test", 111, 111, 200),
        ("try", 111, 111, 409),
        ("test", 111, 112, 409)])
@pytest.mark.asyncio
async def test_change_password_with_auth(Authorized_User, old_password, new_password, confirm_newpassword, status_code):
    data = {
          "old_password": old_password,
          "new_password": new_password,
          "confirm_newpassword": confirm_newpassword


    }
    res = await Authorized_User.post("/user/changepassword", json = data)
    assert res.status_code == status_code


@pytest.mark.asyncio
async def test_change_password_without_auth(async_client):
    data = {
          "old_password": "test",
          "new_password": 111, 
          "confirm_newpassword": 111


    }
    res = await async_client.post("/user/changepassword", json = data)
    assert res.status_code == 401

@pytest.mark.parametrize("id, status_code", [(1,200), (2,404)])
@pytest.mark.asyncio
async def test_profile_with_auth(id: int , status_code, Authorized_User):
    res = await Authorized_User.get(f"/user/{id}")

    assert res.status_code == status_code

@pytest.mark.asyncio
async def test_profile_without_auth(async_client):
    res = await async_client.get(f"/user/{id}")

    assert res.status_code == 401

@pytest.mark.asyncio
async def logout(Authorized_User):
    res = Authorized_User.get("/user/logout")
    
    assert res.status_code == 200
