from app.schemas.base import CustomBaseModel
from pydantic import field_validator
from re import match

class Category(CustomBaseModel):
    name:str
    slug:str


    @field_validator("slug")
    def validate_name(cls,value):
        if not match("^([a-z]|-|_)+$",value):
            raise ValueError("Invalid Slug")
        return value
    
class CategoryOutput(Category):
    id:int

