from datetime import datetime
from typing import Optional
import re
from pydantic import Field, field_validator
from models.base import MassenderBase


class Rol(MassenderBase):
    __tablename__ = "Rol"

    rol_id: Optional[int] = None
    scopes: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=30)

    @field_validator('scopes')
    def validar_scopes(cls, v):
        if v is not None:
            # Expresión regular para validar
            # el formato de scopes
            if not re.match(r'^[A-Za-z]+(,[A-Za-z]+)*$', v):
                raise ValueError('Scopes deben ir separados por coma')
        return v


class RolCreate(Rol):
    descripcion: str = Field(..., max_length=50)
    fecha_insercion: datetime
    usuario_insercion: int


class RolUpdate(Rol):
    rol_id: int
    fecha_modificacion: datetime
    usuario_modificacion: int
