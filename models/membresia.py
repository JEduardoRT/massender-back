
from dataclasses import Field
from typing import Optional
from models.base import MassenderBase


class Membresia(MassenderBase):
    membresia_id: Optional[int]
    titulo: Optional[str] = Field(..., max_length=20)
    descripcion: Optional[str] = Field(..., max_length=100)
    dias_vigencia: Optional[int]