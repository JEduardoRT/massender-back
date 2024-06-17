from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

from models.base import MassenderBase

class ListaDestinatarios(MassenderBase):
    lista_destinatarios_id: Optional[int]
    nombre: Optional[str] = Field(..., max_length=50)
    cliente_id: Optional[int]