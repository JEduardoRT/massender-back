from sqlalchemy import VARCHAR, Column, DateTime, Integer, String
from config.db import Base
from sqlalchemy.orm import relationship
from repository.acceso_rol import AccesoRol


class Rol(Base):
    __tablename__ = 'Rol'

    rol_id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(30), nullable=False)
    scopes = Column(VARCHAR(100), nullable=False)
    estado = Column(String(1), nullable=False)
    fecha_insercion = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    usuario_insercion = Column(Integer, nullable=False)
    usuario_modificacion = Column(Integer, nullable=True)

    accesos = relationship('Acceso', secondary='AccesoRol', back_populates='roles')
