from datetime import datetime
from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    user_id: int
    user_uuid: str
    user_is_enabled: bool
    user_role_type: str
    auth_token_expirationutc: datetime

    class Config:
        from_attributes = True
