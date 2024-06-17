from pydantic import Field
from typing import Optional

from models.base import MassenderBase

class Mensaje(MassenderBase):
    mensaje_id: Optional[int]
    campania_id: Optional[int]
    texto: Optional[str] = Field(..., max_length=60000)
    multimedia: Optional[str] = Field(..., max_length=2000)