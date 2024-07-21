from sqlalchemy import Column, DateTime, Integer, String
from config.db import Base


class TablaPrecios(Base):
    __tablename__ = 'TablaPrecios'

    tabla_precios_id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(50), nullable=False)
    estado = Column(String(1), nullable=False)
    fecha_insercion = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    usuario_insercion = Column(Integer, nullable=False)
    usuario_modificacion = Column(Integer, nullable=True)