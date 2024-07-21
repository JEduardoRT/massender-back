from sqlalchemy import Column, DateTime, Integer, String
from config.db import Base
from sqlalchemy.orm import relationship
from repository.acceso_rol import AccesoRol


class Acceso(Base):
    __tablename__ = 'Acceso'

    acceso_id = Column(Integer, primary_key=True, autoincrement=True)
    ruta = Column(String(100), nullable=False)
    descripcion = Column(String(50), nullable=False)
    estado = Column(String(1), nullable=False)
    fecha_insercion = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    usuario_insercion = Column(Integer, nullable=False)
    usuario_modificacion = Column(Integer, nullable=True)

    roles = relationship('Rol', secondary='AccesoRol', back_populates='accesos')
