from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine
from pydantic import BaseModel
from typing import Optional


personas = Table("persona", meta, 
                 Column("id", Integer, primary_key=True),
                 Column("nombre", String(255)),
                 Column("edad", Integer),
                 Column("correo", String(255)))

meta.create_all(engine)

class Persona(BaseModel):
    id: Optional[int]
    nombre: str
    edad: int
    correo: str