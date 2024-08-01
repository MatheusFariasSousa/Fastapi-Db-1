import pytest
from jose import jwt
from datetime import datetime,timezone,timedelta,UTC
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from app.schemas.user import User
from app.use_cases.user import UserUseCases,SECRET_KEY,ALGORITHM
from app.db.models import User as UserModel
from app.use_cases.user import UserUseCases

crypy_context=CryptContext(schemes=['sha256_crypt'])

def test_register_user(db_session):
    user=User(username="Matheus",password="pass#")
    db=UserUseCases(db_session)
    db.register_user(user=user)

    pessoa =db_session.query(UserModel).first()

    assert pessoa is not None
    assert pessoa.username== user.username
    assert crypy_context.verify(user.password,pessoa.password)
    
    db_session.delete(pessoa)
    db_session.commit()
    
    
def test_register_user_already_exists(db_session,user_on_db):

    db = UserUseCases(db_session)
    user2 =User(username="Matheus",password=crypy_context.hash("12345"))

    with pytest.raises(HTTPException):
        db.register_user(user2)




def test_user_login(db_session,user_on_db):


    uc=UserUseCases(db_session=db_session)
    user=User(
        username="Matheus",
        password="pass#"
    )

    token_data = uc.user_login(user=user,expire_in=30)

    assert token_data.expire_at < datetime.now() + timedelta(31)


def test_user_login_invalid(db_session,user_on_db):


    uc = UserUseCases(db_session=db_session)
    user=User(
        username="Invalid",
        password="pass#"
    )

    with pytest.raises(HTTPException):
        uc.user_login(user=user,expire_in=30)




def test_user_login_password_invalid(db_session,user_on_db):
 
    uc = UserUseCases(db_session=db_session)

    user=User(
        username="Matheus",
        password="Invalid"
    )

    with pytest.raises(HTTPException):
        uc.user_login(user=user,expire_in=30)

def test_verify_token(db_session,user_on_db):
    uc = UserUseCases(db_session=db_session)

    data = {
        "sub": user_on_db.username,
        "exp":datetime.now(UTC) + timedelta(minutes=30)        
    }

    access_token = jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)

    uc.verify_token(token=access_token)
    
def test_verify_token_expire(db_session,user_on_db):
    uc = UserUseCases(db_session=db_session)

    data = {
        "sub": user_on_db.username,
        "exp":datetime.now(UTC) - timedelta(minutes=30)        
    }

    access_token = jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)

    with pytest.raises(HTTPException):

        uc.verify_token(token=access_token)
    


