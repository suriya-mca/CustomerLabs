import uuid
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Dict


class AccountSchema(BaseModel):
    email: EmailStr
    account_name: str
    website: str = None

    class Config:
        from_attributes = True

class AccountResponseSchema(AccountSchema):
    account_id: uuid.UUID
    app_secret_token: str

    class Config:
        from_attributes = True

class DestinationSchema(BaseModel):
    url: str
    http_method: str
    headers: Dict[str, str]

class DestinationResponseSchema(DestinationSchema):
    id: int

    class Config:
        from_attributes = True