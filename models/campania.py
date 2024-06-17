from pydantic import Field
from datetime import date
from typing import Optional

from models.base import MassenderBase

class Campania(MassenderBase):
    campania_id: Optional[int]
    nombre: Optional[str] = Field(..., max_length=50)
    fecha_ini: Optional[date]
    fecha_fin: Optional[date]
    activo: Optional[bool]
    cliente_id: Optional[int]