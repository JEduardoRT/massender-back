from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from utils.constants import ESTADO_ACTIVO, ESTADO_INACTIVO


class MassenderBase(BaseModel):
    estado: Optional[str] = Field(None,
                                  max_length=1,
                                  pattern='^[' + ESTADO_ACTIVO
                                  + ESTADO_INACTIVO + ']$')
    fecha_insercion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None
    usuario_insercion: Optional[int] = None
    usuario_modificacion: Optional[int] = None

    class Config:
        from_attributes = True
