import asyncio
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.db import get_session


from tests.db import async_engine
from app.main import app


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
   loop = asyncio.get_event_loop_policy().new_event_loop()
   yield loop
   loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
   session = sessionmaker(
       async_engine, class_=AsyncSession, expire_on_commit=False
   )

   async with async_engine.begin() as conn:
       await conn.run_sync(SQLModel.metadata.drop_all)

   async with session() as s:
       async with async_engine.begin() as conn:
           await conn.run_sync(SQLModel.metadata.create_all)

       yield s

   

   #await async_engine.dispose()


@pytest_asyncio.fixture
async def async_client(async_session):

    async def override_get_db():
        try:
            yield async_session
        finally:
            await async_session.close()
    app.dependency_overrides[get_session] = override_get_db

    async with AsyncClient(
           app=app,
           base_url=f"http://"
   ) as client:
       yield client


@pytest_asyncio.fixture
async def user1(async_client: AsyncClient):
    data = {"email":"lawalafeez820@gmail.com","password": "test", "confirm_password": "test", "user_name": "lawal"}
    res = await async_client.post("/user/", json = data)
    res = res.json()
    res["password"] = data["password"]
    return res

@pytest_asyncio.fixture
async def user2(async_client: AsyncClient):
    data = {"email":"lawalafeez8202@gmail.com","password": "test2", "confirm_password": "test2", "user_name": "lawala"}
    res = await async_client.post("/user/", json = data)
    res = res.json()
    res["password"] = data["password"]
    return res

@pytest_asyncio.fixture
async def Authorized_User(user1, async_client):
    data = {"username":"lawalafeez820@gmail.com","password": "test"}
    res = await async_client.post("/login", data = data)
    res = res.json()
    async_client.headers ={**async_client.headers, "Authorization": f"Bearer {res['access_token']}"}
    return async_client

@pytest_asyncio.fixture
async def Authorized_User2(user2, async_client):
    data = {"username":"lawalafeez8202@gmail.com","password": "test2"}
    res = await async_client.post("/login", data = data)
    res = res.json()
    async_client.headers ={**async_client.headers, "Authorization": f"Bearer {res['access_token']}"}
    return async_client


@pytest_asyncio.fixture
async def post(Authorized_User):

    data={
         "title": "real",
    "content":"too real",
    "publish" : True
    }
    res= await Authorized_User.post("/post/", json= data)

    return res.json()

@pytest_asyncio.fixture
async def comment(Authorized_User, post):
    data={
      "comment": "commenting"
    }
    res = await Authorized_User.post(f"/comment/1", json= data)
    return res.json()

@pytest_asyncio.fixture
async def vote(Authorized_User2, post):
    data={
      "votedir": 1
    }
    res = await Authorized_User2.post(f"/like/1", json= data)
    return res.json()




    








