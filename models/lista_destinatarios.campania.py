from typing import Optional

from models.base import MassenderBase

class ListaDestinatariosCampania(MassenderBase):
    campania_id: Optional[int]
    lista_destinatarios_id: Optional[int]