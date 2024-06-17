from typing import Optional

from pydantic import Field

from models.base import MassenderBase


class Rol(MassenderBase):
    rol_id: Optional[int]
    descripcion: Optional[str] = Field(..., max_length=30)