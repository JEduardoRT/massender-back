from pydantic import Field
from datetime import date, datetime
from typing import Optional

from models.base import MassenderBase


class Pago(MassenderBase):
    pago_id: Optional[int] = None
    cliente_id: Optional[int] = None
    membresia_id: Optional[int] = None
    fecha_pago: Optional[date] = None
    pagado: Optional[bool] = None
    cod_medio_pago: Optional[str] = Field(None,
                                          max_length=3,
                                          pattern=r'^[A-Z]{3}$')


class PagoCreate(Pago):
    cliente_id: int
    membresia_id: int
    fecha_pago: date
    pagado: bool
    cod_medio_pago: str = Field(...,
                                max_length=3,
                                pattern=r'^[A-Z]{3}$')
    fecha_insercion: datetime
    usuario_insercion: int


class PagoUpdate(Pago):
    pago_id: int
    fecha_modificacion: datetime
    usuario_modificacion: int
