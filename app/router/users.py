from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select
from app.models.users import User, CreateUser, UserOut, LoginCred, PasswordData, PlainText, UserData
from app.database.db import get_session
from app.Password_Manager.password import password
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.OAuth.oauth import Token_Data, oauth_data, BLACKLIST
from pydantic import EmailStr
from typing import List

app = APIRouter(
    tags = ["User"],
    prefix ="/user"
)

#create account
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

#get all users
@app.get("/all", response_model=List[UserOut])
async def get_all_user(limit:int= 5, offset:int = 0, user: User = Depends(Token_Data.get_current_user), db: Session = Depends(get_session)):
    members = await db.exec(select(User).limit(limit).offset(offset).order_by(User.user_name))
    members:List[User] |None = members.all()
   

    if not user:
        raise HTTPException(404, detail= f"There is no user at the moment")
        
    return members


#change passsword
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



#get a particular user by id

@app.get("/{id}", response_model = UserData)
async def profile(id: int, user: User = Depends(Token_Data.get_current_user), db: Session = Depends(get_session)):

    
     
    if id == user.id:
        return user
    part_user = await db.get(User, id)
    
    if not part_user:
        raise HTTPException(404, detail= f"No user with an id {id}")
   
    return part_user


#logout

@app.get("/logout", response_model=PlainText)
async def logout(auth:str= Depends(oauth_data)):
    BLACKLIST.add(auth)
    return PlainText(detail="You have sucessfully logged out")



    



    
    