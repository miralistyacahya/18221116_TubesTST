from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class User(BaseModel):
    username: str
    name: str
    email: str
    password: str

    class config:
        json_schema_extra = {
            "example": {
                "username": "rarara",
                "name": "rara",
                "email": "miralistya@gmail.com",
                "password": "rr123"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

class UserOut(BaseModel):
    id: UUID
    email: str

class SystemUser(UserOut):
    password: str