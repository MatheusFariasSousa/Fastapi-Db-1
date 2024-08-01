from sqlalchemy.orm import Session
from jose import jwt,JWTError
from datetime import datetime,timedelta
from fastapi.exceptions import HTTPException
from fastapi import status
from app.db.models import User as UserModel
from app.schemas.user import User
from app.schemas.token import TokenData
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

cryp_context=CryptContext(schemes=["sha256_crypt"])
SECRET_KEY="5178fc5037fea93a378885bef2b08076fd20e737ad75077e03949494c02520df"
ALGORITHM="HS256"



class UserUseCases:
    def __init__(self,db_session:Session):
        self.db_session=db_session


    def register_user(self,user:User):
        user_on_db =UserModel(
            username=user.username,
            password=cryp_context.hash(user.password)
        )
        self.db_session.add(user_on_db)
        try:
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="This name alread exists")
        
    
    def user_login(self,user:User,expire_in:int=30):
        user_on_db= self._get_user(username=user.username)

        if user_on_db is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authorized")
        if not cryp_context.verify(user.password,user_on_db.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authorized")
        
        expire_at = datetime.now()+timedelta(expire_in)

        data={
            "sub":user_on_db.username,
            "exp":expire_at
        }

        acess_token=jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)

        token_data= TokenData(acess_token=acess_token,expire_at=expire_at)

        return token_data
    
    def verify_token(self,token:str):
        try:
            data = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token")
        
        user_on_db = self._get_user(username=data["sub"])
        if user_on_db is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token")



    def _get_user(self,username:str):
        user_on_db=self.db_session.query(UserModel).where(UserModel.username==username).first()

        return user_on_db



        



