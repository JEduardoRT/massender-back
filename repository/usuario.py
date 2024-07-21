from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, Integer, String
from config.db import Base


class Usuario(Base):
    __tablename__ = 'Usuario'

    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(10), nullable=False)
    nombre_completo = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    correo = Column(String(30), nullable=False)
    rol_id = Column(Integer, ForeignKey('rol.rol_id'), nullable=False)
    cliente_id = Column(Integer, ForeignKey('cliente.cliente_id'), nullable=True)
    telefono = Column(VARCHAR(15), nullable=False)
    estado = Column(String(1), nullable=False)
    fecha_insercion = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    usuario_insercion = Column(Integer, nullable=False)
    usuario_modificacion = Column(Integer, nullable=True)