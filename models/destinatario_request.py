import re
from pydantic import BaseModel, EmailStr, Field, validator, field_validator
from typing import Optional


class DestinatarioRequest(BaseModel):
    cedula: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=20)
    apellido: str = Field(..., max_length=20)
    genero: str = Field(..., max_length=1)
    correo: EmailStr = Field(..., max_length=50)
    telefono: Optional[str] = Field(None, max_length=15)

    @field_validator('telefono')
    def validar_telefono(cls, v):
        if v is not None and not re.match(r'^\d{1,3}\d{,14}$', v):
            raise ValueError('El número de teléfono no es válido')
        return v
