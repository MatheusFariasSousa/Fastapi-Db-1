from app.schemas.user import User
import pytest

def test_valid_user_schema():
    user=User(username="Matheus",password="123456")
    
    assert user.dict()== {"username":"Matheus","password":"123456"}

def test_invalid_user_schema_name():
    with pytest.raises(ValueError):
        user=User(username="Mãtheus@",password="12345")