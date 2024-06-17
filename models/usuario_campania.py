from typing import Optional

from models.base import MassenderBase

class UsuarioCampania(MassenderBase):
    usuario_id: Optional[int]
    campania_id: Optional[int]