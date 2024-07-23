from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status
from app.db.models import User as UserModel
from app.schemas.user import User
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

cryp_context=CryptContext(schemes=["sha256_crypt"])

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
        except:
            self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="This name alread exists")

        



