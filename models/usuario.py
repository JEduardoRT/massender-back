import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class Usuario(BaseModel):
    usuario_id: Optional[int]
    username: Optional[str] = Field(..., max_length=10)
    nombre_completo: Optional[str] = Field(..., max_length=50)
    password: Optional[str] = Field(..., max_length=50)
    correo: Optional[EmailStr] = Field(..., max_length=30)
    rol_id: Optional[int]
    cliente_id: Optional[int]
    telefono: Optional[str] = Field(..., max_length=15)

    @field_validator('telefono')
    def validar_telefono(cls, v):
        if v is not None:
            # Expresión regular para validar el formato de un número de teléfono
            if not re.match(r'^\d{1,3}\d{,14}$', v):
                raise ValueError('El número de teléfono no es un usuario ')
        return v
    
    @field_validator('username')
    def validar_username(cls, v):
        if v is not None:
            if not re.match(r'^[\w.]+$', v):
                raise ValueError('No es un usuario válido')
        return v