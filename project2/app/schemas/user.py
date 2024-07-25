from app.schemas.base import CustomBaseModel
from pydantic import field_validator
import re

class User(CustomBaseModel):
    username:str
    password:str

    @field_validator("username")
    def name_validator(cls,value):
        if not re.match("^([a-z]|[A-Z]|[0-9]|-|_||@)+$",value):
            raise ValueError("This username is invalid")
        return value
    
class UserOutput(User):
    id:int
    

