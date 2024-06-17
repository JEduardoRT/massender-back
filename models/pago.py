from pydantic import Field
from datetime import date
from typing import Optional

from models.base import MassenderBase

class Pago(MassenderBase):
    pago_id: Optional[int]
    cliente_id: Optional[int]
    membresia_id: Optional[int]
    fecha_pago: Optional[date]
    pagado: Optional[bool]
    cod_medio_pago: Optional[str] = Field(..., max_length=3, pattern=r'^[A-Z]{3}$')