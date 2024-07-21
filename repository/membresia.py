from sqlalchemy import Column, DateTime, Integer, String
from config.db import Base


class Membresia(Base):
    __tablename__ = 'Membresia'

    membresia_id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(20), nullable=False)
    descripcion = Column(String(100), nullable=False)
    dias_vigencia = Column(Integer, nullable=False)
    estado = Column(String(1), nullable=False)
    fecha_insercion = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    usuario_insercion = Column(Integer, nullable=False)
    usuario_modificacion = Column(Integer, nullable=True)