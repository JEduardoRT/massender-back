
from datetime import datetime
from typing import Optional

from pydantic import Field
from models.base import MassenderBase


class TablaPrecios(MassenderBase):
    tabla_precios_id: Optional[int]
    descripcion: Optional[str] = Field(..., max_length=50)