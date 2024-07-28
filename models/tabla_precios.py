
from datetime import datetime
from typing import Optional

from pydantic import Field
from models.base import MassenderBase


class TablaPrecios(MassenderBase):
    tabla_precios_id: Optional[int] = None
    descripcion: Optional[str] = Field(None, max_length=50)


class TablaPreciosCreate(TablaPrecios):
    descripcion: str = Field(..., max_length=50)
    fecha_insercion: datetime
    usuario_insercion: int


class TablaPreciosUpdate(TablaPrecios):
    tabla_precios_id: int
    fecha_modificacion: datetime
    usuario_modificacion: int
