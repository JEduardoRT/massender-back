from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from config.db import Base


class Precio(Base):
    __tablename__ = 'Precio'

    precio_id = Column(Integer, primary_key=True, autoincrement=True)
    membresia_id = Column(Integer, ForeignKey('Membresia.membresia_id'), nullable=False)
    tabla_precios_id = Column(Integer, ForeignKey('Tabla_precios.tabla_precios_id'), nullable=False)
    valor = Column(Float, nullable=False)
    estado = Column(String(1), nullable=False)
    fecha_insercion = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    usuario_insercion = Column(Integer, nullable=False)
    usuario_modificacion = Column(Integer, nullable=True)