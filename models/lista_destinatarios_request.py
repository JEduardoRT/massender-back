from pydantic import BaseModel, Field
from typing import List, Optional
from models.destinatario_request import DestinatarioRequest


class ListaDestinatariosRequest(BaseModel):
    nombreLista: str = Field(..., max_length=50)
    destinatarios: List[DestinatarioRequest]
