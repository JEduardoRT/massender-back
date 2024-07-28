from typing import List
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    user_id: int


class TokenData(BaseModel):
    username: str | None = None
    scopes: List[str] = []
