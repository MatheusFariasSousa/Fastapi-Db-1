import pytest
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from app.schemas.user import User

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
    
    
def test_register_user_already_exists(db_session):
    user=UserModel(username="Matheus",password=crypy_context.hash("pass#"))
    

    db_session.add(user)
    db_session.commit()
    db = UserUseCases(db_session)
    user2 =User(username="Matheus",password=crypy_context.hash("12345"))

    with pytest.raises(HTTPException):
        db.register_user(user2)


    db_session.delete(user)
    db_session.commit()