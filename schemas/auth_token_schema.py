from datetime import datetime
from pydantic import BaseModel


class AuthorizeUserDto(BaseModel):
    email_address: str
    password: str

    class Config:
        from_attribute = True


class AuthTokenAdd(BaseModel):
    user_id: int
    auth_token: str
    auth_token_expirationutc: datetime

    class Config:
        from_attribute = True
