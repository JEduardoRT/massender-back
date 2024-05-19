from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    id: int

    descripcion: Optional[str] = Field(default="Producto nuevo", min_length=10, max_length=100)

    valor: Optional[float] = Field(default=0, gt=0)