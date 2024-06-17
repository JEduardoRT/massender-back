from typing import Optional

from models.base import MassenderBase

class Precio(MassenderBase):
    precio_id: Optional[int]
    membresia_id: Optional[int]
    tabla_precios_id: Optional[int]
    valor: Optional[float]