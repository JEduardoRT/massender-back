from pydantic import Field
from datetime import datetime
from typing import Optional

from models.base import MassenderBase


class MedioPago(MassenderBase):
    medio_pago_id: Optional[int] = None
    descripcion: Optional[str] = Field(None, max_length=50)
    codigo: Optional[str] = Field(None, max_length=3, pattern=r'^[A-Z]{3}$')


class MedioPagoCreate(MedioPago):
    descripcion: str = Field(..., max_length=50)
    codigo: str = Field(..., max_length=3, pattern=r'^[A-Z]{3}$')
    fecha_insercion: datetime
    usuario_insercion: int


class MedioPagoUpdate(MedioPago):
    medio_pago_id: int
    fecha_modificacion: datetime
    usuario_modificacion: int
