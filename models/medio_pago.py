
from dataclasses import Field
from typing import Optional
from models.base import MassenderBase


class MedioPago(MassenderBase):
    medio_pago_id: Optional[int]
    descripcion: Optional[str] = Field(..., max_length=50)
    codigo: Optional[str] = Field(..., max_length=3, pattern=r'^[A-Z]{3}$')