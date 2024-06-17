from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from utils.constants import ESTADO_ACTIVO, ESTADO_INACTIVO


class MassenderBase(BaseModel) :
    
    estado: str = Field(..., max_length=1, pattern='^['+ESTADO_ACTIVO+ESTADO_INACTIVO+']$')
    fecha_insercion: Optional[datetime]
    fecha_modificacion: Optional[datetime]
    usuario_insercion: Optional[int]
    usuario_modificacion: Optional[int]