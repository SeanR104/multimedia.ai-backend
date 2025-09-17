import uuid

from pydantic import BaseModel, model_validator
from system.exceptions import EFBadRequestException


class UserBase(BaseModel):
    email_address: str
    first_name: str
    last_name: str
    user_role_type: str

    class Config:
        from_attribute = True


class UserView(UserBase):
    pass


class UserAdd(UserBase):
    new_password1: str
    new_password2: str
    user_is_enabled: bool = False
    user_is_deleted: bool = False
    user_uuid: str = str(uuid.uuid4())

    def for_db(self):
        return self.model_dump(exclude={'new_password1', 'new_password2'})

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserAdd':
        if self.new_password1 != self.new_password2:
            raise EFBadRequestException('Passwords do not match')
        return self


class UserEdit(UserBase):
    user_id: int
    user_is_enabled: bool


class UserRemove(UserBase):
    user_id: int
    user_is_deleted: bool = True
