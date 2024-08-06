from datetime import datetime
import re
from pydantic import Field, field_validator
from typing import Optional

from models.base import MassenderBase


class Acceso(MassenderBase):
    acceso_id: Optional[int] = None
    ruta: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=50)

    @field_validator('ruta')
    def validar_ruta(cls, v):
        if v is not None:
            # Expresión regular para validar
            # el formato de un número de teléfono
            if not re.match(r'^/*\w+(/:*\w+)*$', v):
                raise ValueError('La ruta no es válida')
        return v


class AccesoCreate(Acceso):
    ruta: str = Field(..., max_length=100)
    descripcion: str = Field(..., max_length=50)
    fecha_insercion: datetime
    usuario_insercion: int


class AccesoUpdate(Acceso):
    acceso_id: int
    fecha_modificacion: datetime
    usuario_modificacion: int
