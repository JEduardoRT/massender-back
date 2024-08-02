from pydantic import Field
from datetime import datetime
from typing import Optional

from models.base import MassenderBase


class Mensaje(MassenderBase):
    mensaje_id: Optional[int] = None
    campania_id: Optional[int] = None
    texto: Optional[str] = Field(None, max_length=60000)
    multimedia: Optional[str] = Field(None, max_length=2000)


class MensajeCreate(Mensaje):
    campania_id: int
    texto: str = Field(..., max_length=60000)
    multimedia: str = Field(..., max_length=2000)


class MensajeUpdate(Mensaje):
    mensaje_id: int
    fecha_modificacion: datetime
    usuario_modificacion: int
