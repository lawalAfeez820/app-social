from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select
from app.models.users import User, CreateUser, UserOut, LoginCred, PasswordData, PlainText, UserData
from app.database.db import get_session
from typing import Annotated
from app.Password_Manager.password import password
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.OAuth.oauth import Token_Data, oauth_data, BLACKLIST
from pydantic import EmailStr

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



@app.post("/changepassword", response_model = PlainText)
async def change_password(Password: PasswordData, db: Session = Depends(get_session), user :User = Depends(Token_Data.get_current_user)):
    if not password.verify_hash(Password.old_password, user.password):
        raise HTTPException(status_code= 409, detail = "You have entered a wrong old password")
    if not password.verify_plain(Password.new_password, Password.confirm_newpassword):
        raise HTTPException(status_code= 409, detail = "New password field and confirm_newpassword field must be the same")
    user.password = password.hash_ps(Password.new_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return PlainText(detail = "Password Changed Successfully")


@app.get("/{id}", response_model = UserData)
async def profile(id: int, user: User = Depends(Token_Data.get_current_user), db: Session = Depends(get_session)):

    if not id:
        raise HTTPException(404, detail= f"No user with an id {id}")
     
    if id == user.id:
        return user
    part_user = await db.get(User, id)
   
    return part_user

@app.get("/all", response_model = UserOut)
async def get_all_user(User = Depends(Token_Data.get_current_user), db: Session = Depends(get_session)):
    users: User= await db.exec(select(User)).mimit(limit).offset(offset)
    users = users.all()
   

    if not users:
        raise HTTPException(404, detail= f"There is no user at the moment")
        
    return users





@app.get("/logout", response_model=PlainText)
async def logout(auth:str= Depends(oauth_data)):
    BLACKLIST.add(auth)
    return PlainText(detail="You have sucessfully logged out")



    



    
    