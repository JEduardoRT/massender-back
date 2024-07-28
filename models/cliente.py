from pydantic import Field
from datetime import date, datetime
from typing import Optional

from models.base import MassenderBase


class Cliente(MassenderBase):
    cliente_id: Optional[int] = None
    nombre: Optional[str] = Field(None, max_length=20)
    membresia_id: Optional[int] = None
    tabla_precios_id: Optional[int] = None
    medio_pago_id: Optional[int] = None
    fecha_ini_memb: Optional[date] = None
    fecha_fin_memb: Optional[date] = None


class ClienteCreate(Cliente):
    nombre: str = Field(..., max_length=20)
    tabla_precios_id: int
    medio_pago_id: int
    fecha_insercion: datetime
    usuario_insercion: int


class ClienteUpdate(Cliente):
    cliente_id: int
    fecha_modificacion: datetime
    usuario_modificacion: int
