from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from config.db import Base


class Campania(Base):
    __tablename__ = 'Campania'

    campania_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    fecha_ini = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    activo = Column(Boolean, nullable=False)
    cliente_id = Column(Integer, ForeignKey('Cliente.cliente_id'), nullable=False)
    estado = Column(String(1), nullable=False)
    fecha_insercion = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    usuario_insercion = Column(Integer, nullable=False)
    usuario_modificacion = Column(Integer, nullable=True)