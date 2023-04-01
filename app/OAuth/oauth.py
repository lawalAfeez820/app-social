from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from jose import JWTError, jwt
from typing import Dict
from sqlmodel import Session, select
from pydantic import EmailStr
from app.config.config import setting
from app.models.users import User
from datetime import timedelta, datetime
from app.database.db import get_session

oauth_data = OAuth2PasswordBearer(tokenUrl = "user/me")


class Token:

    def get_access_token(self, payload: Dict):

        data = payload.copy()
        data["exp"] = datetime.utcnow() + timedelta(minutes = setting.expiry_time)

        token: str = jwt.encode(data, setting.secret_key, algorithm = setting.algorithm)
        
        return token
    
    def verify_access_token(self, token: str, credentials_exception):
        try:

            data = jwt.decode(token, setting.secret_key, algorithms=[setting.algorithm])
            email : EmailStr = data.get("email")

        except JWTError:
            raise credentials_exception
        return email
    
    async def get_current_user(self, token: str = Depends(oauth_data), db: Session = Depends(get_session)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},)
         
        email: EmailStr = self.verify_access_token(token, credentials_exception)
       
        user = await db.exec(select(User).where(User.email == email))
        user: User = user.first()
        return user





Token_Data = Token()
