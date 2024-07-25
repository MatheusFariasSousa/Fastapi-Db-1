from app.schemas.base import CustomBaseModel
from datetime import datetime


class TokenData(CustomBaseModel):
    acess_token:str
    expire_at:datetime
