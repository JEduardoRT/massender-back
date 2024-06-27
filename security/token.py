from typing import List, Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: List[str] = []

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class Rol(BaseModel):
    scopes: List[str] = []


class UserInDB(User):
    hashed_password: str
    rol: Rol = None
