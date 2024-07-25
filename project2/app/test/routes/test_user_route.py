from app.schemas.user import User
from fastapi.testclient import TestClient
from app.db.models import User as UserModel

from app.main import app
from fastapi import status





client=TestClient(app)

def test_post_user(db_session):
    
    user={"username":"Matheus","password":"1234"}
    
    response = client.post("/user/post",json=user)

    

    assert response.status_code==status.HTTP_201_CREATED

    pessoa = db_session.query(UserModel).first()
    
    db_session.delete(pessoa)
    db_session.commit()

def test_post_user_already_exists(db_session):
    user_on_db=UserModel(username="Matheus",password="1234")
    db_session.add(user_on_db)
    db_session.commit()
    db_session.refresh(user_on_db)

    user={"username":"Matheus","password":"12345"}
    response = client.post("/user/post",json=user)

    assert response.status_code==status.HTTP_400_BAD_REQUEST

    db_session.delete(user_on_db)
    db_session.commit()


def test_user_login_route(user_on_db):
    body={
        "username":user_on_db.username,
        "password":"pass#"
    }

    headers = {"Contex-Type":"application/x-www-form-urlencoded"}

    response = client.post("/user/login",data=body,headers=headers)    


    assert response.status_code == status.HTTP_200_OK

    data= response.json()

    assert "acess_token" in data

    assert "expire_at" in data

def test_user_login_route_invalid_username(user_on_db):
    body={
        "username":"Invalid",
        "password":"pass#"
    }

    headers = {"Contex-Type":"application/x-www-form-urlencoded"}

    response = client.post("/user/login",data=body,headers=headers)    


    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_login_route_invalid_password(user_on_db):
    body={
        "username":"Matheus",
        "password":"pass#1"
    }

    headers = {"Contex-Type":"application/x-www-form-urlencoded"}

    response = client.post("/user/login",data=body,headers=headers)    


    assert response.status_code == status.HTTP_401_UNAUTHORIZED



