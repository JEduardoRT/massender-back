from datetime import datetime
from pydantic import Field
from typing import Optional

from models.base import MassenderBase


class Membresia(MassenderBase):
    membresia_id: Optional[int] = None
    titulo: Optional[str] = Field(None, max_length=20)
    descripcion: Optional[str] = Field(None, max_length=100)
    dias_vigencia: Optional[int] = None


class MembresiaCreate(Membresia):
    titulo: str = Field(..., max_length=20)
    descripcion: str = Field(..., max_length=20)
    dias_vigencia: int
    fecha_insercion: datetime
    usuario_insercion: int


class MembresiaUpdate(Membresia):
    membresia_id: int
    fecha_modificacion: datetime
    usuario_modificacion: int
