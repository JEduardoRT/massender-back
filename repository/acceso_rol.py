from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from config.db import Base


class AccesoRol(Base):
    __tablename__ = 'AccesoRol'

    acc_rol_id = Column(Integer, primary_key=True, autoincrement=True)
    acceso_id = Column(Integer, ForeignKey('Acceso.acceso_id'), nullable=False)
    rol_id = Column(Integer, ForeignKey('Rol.rol_id'), nullable=False)
    estado = Column(String(1), nullable=False)
    fecha_insercion = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    usuario_insercion = Column(Integer, nullable=False)
    usuario_modificacion = Column(Integer, nullable=True)
