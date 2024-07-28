from datetime import datetime
import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

from models.rol import Rol


class Usuario(BaseModel):
    usuario_id: Optional[int] = None
    username: Optional[str] = Field(None, max_length=10)
    nombre_completo: Optional[str] = Field(None, max_length=50)
    correo: Optional[EmailStr] = Field(None, max_length=30)
    rol_id: Optional[int] = None
    cliente_id: Optional[int] = None
    telefono: Optional[str] = Field(None, max_length=15)
    rol: Optional[Rol] = None

    @field_validator('telefono')
    def validar_telefono(cls, v):
        if v is not None:
            # Expresión regular para validar el
            # formato de un número de teléfono
            if not re.match(r'^\d{1,3}\d{,14}$', v):
                raise ValueError('El número de teléfono no es válido')
        return v

    @field_validator('username')
    def validar_username(cls, v):
        if v is not None:
            if not re.match(r'^[\w.]+$', v):
                raise ValueError('No es un usuario válido')
        return v


class UsuarioCreate(Usuario):
    username: str = Field(..., max_length=10)
    nombre_completo: str = Field(..., max_length=50)
    password: str = Field(..., max_length=60)
    correo: EmailStr = Field(..., max_length=30)
    rol_id: int
    cliente_id: int
    telefono: str = Field(..., max_length=15)
    fecha_insercion: datetime
    usuario_insercion: int


class UsuarioUpdate(Usuario):
    usuario_id: int
    password: Optional[str] = Field(None, max_length=60)
    fecha_modificacion: datetime
    usuario_modificacion: int
