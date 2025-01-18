from datetime import datetime

from pydantic import BaseModel


class OwnerRequestModel(BaseModel):
    email: str
    password: str


class TokenModel(BaseModel):
    access_token: str
    token_type: str
    message: str

class OwnerImageModel(BaseModel):
    id: int
    owner_email: str
    image_data: bytes
    created_at: datetime
