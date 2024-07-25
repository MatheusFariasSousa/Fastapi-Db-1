from app.schemas.user import User
from app.use_cases.user import UserUseCases
from app.routes.deps import get_db_session
from fastapi import Depends,status,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session




router=APIRouter(prefix="/user",tags=["User"])

@router.post("/post",status_code=status.HTTP_201_CREATED)
def add_user(user:User,session:Session = Depends(get_db_session)):
    uc=UserUseCases(db_session=session)
    uc.register_user(user=user)
    
    return status.HTTP_201_CREATED

@router.post("/login")
def user_login(login_request_form:OAuth2PasswordRequestForm=Depends(),
               session:Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=session)

    user = User(
        username= login_request_form.username,
        password=login_request_form.password
    )
    token_data = uc.user_login(user=user,expire_in=32)

    return token_data



