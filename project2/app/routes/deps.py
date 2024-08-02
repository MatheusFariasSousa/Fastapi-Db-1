from fastapi import Depends
from app.db.connection import Session
from fastapi.security import OAuth2PasswordBearer
from app.use_cases.user import UserUseCases
from sqlalchemy.orm import Session as Sessionn



oaut_scheme =OAuth2PasswordBearer(tokenUrl="/user/login")




def get_db_session():
    try:
        session =Session()
        yield session
    finally:
        session.close()

def oauth(db_session:Sessionn=Depends(get_db_session),token = Depends(oaut_scheme)):
   
    uc = UserUseCases(db_session=db_session)

    uc.verify_token(token=token)
    

