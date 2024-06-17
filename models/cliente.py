from pydantic import Field
from datetime import date
from typing import Optional

from models.base import MassenderBase

class Cliente(MassenderBase):
    cliente_id: Optional[int]
    nombre: Optional[str] = Field(..., max_length=20)
    membresia_id: Optional[int]
    tabla_precios_id: Optional[int]
    medio_pago_id: Optional[int]
    fecha_ini_memb: Optional[date]
    fecha_fin_memb: Optional[date]