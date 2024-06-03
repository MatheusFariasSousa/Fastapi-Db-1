from app.schemas.base import CustomBaseModel
from app.schemas.category import Category
from re import match 
from pydantic import field_validator

class Product(CustomBaseModel):
    name:str
    slug:str
    price:float
    stock:int


    @field_validator("slug")
    def validate_slug(cls,value):
        if not match("^([a-z]|-|_)+$",value):
            raise ValueError("Invalid Slug")
        return value
    
    @field_validator("price")
    def validate_price(cls,price):
        if price<=0:
            raise ValueError("Invalid Price")
        return price
    


class ProductInput(CustomBaseModel):
    category_slug:str
    product:Product


class ProductOutput(Product):
    id:int
    category:Category
