from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select
from app.models.users import User, CreateUser, UserOut, LoginCred
from app.database.db import get_session
from typing import Annotated
from app.Password_Manager.password import password
from fastapi.security import OAuth2PasswordRequestForm
from app.OAuth.oauth import Token_Data

app = APIRouter(
    tags = ["User"],
    prefix ="/user"
)

@app.post("/", response_model = UserOut, status_code= 201)
async def create_user(data: CreateUser, db: Session = Depends(get_session)):

    # if user type the same pasword for the two password field while registering
    if not password.verify_plain(data.confirm_password, data.password):
        raise HTTPException(status_code = 403, detail= f"You didn't enter the same password for password and confirm_password field")
    
    #hash the password
    data.password = password.hash_ps(data.password)

    #check for duplicate email
    user: User | None = await db.exec(select(User).where(User.email == data.email))
    
    if user.first():
        raise HTTPException(status_code = 409, detail= f"User with email `{data.email}` already exist")
   
    #check for username
    user: User | None =await db.exec(select(User).where(User.user_name == data.user_name))
    if user.first():
        raise HTTPException(status_code = 409, detail= f"User with username `{data.user_name}` already exist")

    # add user to database
    data = User.from_orm(data)
    db.add(data)
    await db.commit()
    await db.refresh(data)
    
    return data

@app.post("/me", response_model = LoginCred)
async def Login(details:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = await db.exec(select(User).where(User.email == details.username))
  
    user: User | None = user.first()

    if not user:
        raise HTTPException(status_code= 409, detail = "Incorrect Email or password")
    
    
    if not password.verify_hash(details.password, user.password):
        raise HTTPException(status_code= 409, detail = "Incorrect Email or password")
    
    token:str = Token_Data.get_access_token({"email": details.username})
    return LoginCred(access_token = token, token_type = "bearer")