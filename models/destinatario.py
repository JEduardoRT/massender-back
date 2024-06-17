import re
from pydantic import EmailStr, Field, field_validator
from typing import Optional

from models.base import MassenderBase

class Destinatario(MassenderBase):
    destinatario_id: Optional[int]
    nombre_completo: Optional[str] = Field(..., max_length=20)
    correo: Optional[EmailStr] = Field(..., max_length=50)
    telefono: Optional[str] = Field(None, max_length=15)
    metadatos: Optional[str] = Field(None, max_length=500)
    lista_id: Optional[int]

    @field_validator('telefono')
    def validar_telefono(cls, v):
        if v is not None:
            # Expresión regular para validar el formato de un número de teléfono
            if not re.match(r'^\d{1,3}\d{,14}$', v):
                raise ValueError('El número de teléfono no es válido')
        return v