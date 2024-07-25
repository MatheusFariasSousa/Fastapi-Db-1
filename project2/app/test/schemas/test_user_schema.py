from app.schemas.token import TokenData
from app.schemas.user import User
from datetime import datetime
import pytest

def test_valid_user_schema():
    user=User(username="Matheus",password="123456")
    
    assert user.dict()== {"username":"Matheus","password":"123456"}

def test_invalid_user_schema_name():
    with pytest.raises(ValueError):
        user=User(username="Mãtheus@",password="12345")

def test_toke_schema():
    expire_at=datetime.now()
    token=TokenData(
        acess_token="token",
        expire_at=expire_at
    )
    assert token.dict()=={"acess_token":"token","expire_at":expire_at}

