from pydantic import BaseModel
from datetime import datetime


class ApiKeyAdd(BaseModel):
    name: str


class ApiKeyView(BaseModel):
    api_key_id: int
    key_value: str
    name: str
    is_active: bool
    createdutc: datetime
    updatedutc: datetime | None = None
    last_used_utc: datetime | None = None
    revokedutc: datetime | None = None
