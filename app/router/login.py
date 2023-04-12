from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select
from app.models.users import User, PlainText, LoginCred, ForgetPassword
from app.database.db import get_session
from app.Password_Manager.password import password
from app.OAuth.oauth import Token_Data
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.engine.result import ScalarResult
app = APIRouter()


#forget password route
@app.post("/forgetpassword", response_model=PlainText)
async def forgetpin(Password:ForgetPassword, db: Session= Depends(get_session)):

    user: ScalarResult= await db.exec(select(User).where(User.email == Password.email))
    user : User = user.first()
    if not user:
        raise HTTPException(status_code= 409, detail = f"No User with an email {Password.email}")
    user.password = password.hash_ps(user.email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return PlainText(detail = f"Your password has been reset to your mail")

#login
@app.post("/login", response_model = LoginCred)
async def Login(details:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user: ScalarResult = await db.exec(select(User).where(User.email == details.username))
  
    user: User | None = user.first()

    if not user:
        raise HTTPException(status_code= 409, detail = "Incorrect Email or password")
    
    
    if not password.verify_hash(details.password, user.password):
        raise HTTPException(status_code= 409, detail = "Incorrect Email or password")
    
    token:str = Token_Data.get_access_token({"email": details.username})
    return LoginCred(access_token = token, token_type = "bearer")