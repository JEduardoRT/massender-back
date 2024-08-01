from datetime import datetime
from typing import Optional

from models.base import MassenderBase


class Precio(MassenderBase):
    precio_id: Optional[int]
    membresia_id: Optional[int]
    tabla_precios_id: Optional[int]
    valor: Optional[float]


class PrecioCreate(Precio):
    membresia_id: int
    tabla_precios_id: int
    valor: float
    fecha_insercion: datetime
    usuario_insercion: int


class PrecioUpdate(Precio):
    precio_id: int
    fecha_modificacion: datetime
    usuario_modificacion: int
