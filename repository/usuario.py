from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, Integer, String
from config.db import Base
from sqlalchemy.orm import relationship, Session, selectinload

from utils.constants import ESTADO_ACTIVO


class Usuario(Base):
    __tablename__ = 'Usuario'

    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(10), nullable=False)
    nombre_completo = Column(String(50), nullable=False)
    password = Column(String(60), nullable=False)
    correo = Column(String(30), nullable=False)
    rol_id = Column(Integer, ForeignKey('Rol.rol_id'), nullable=False)
    cliente_id = Column(Integer, ForeignKey('Cliente.cliente_id'),
                        nullable=True)
    telefono = Column(VARCHAR(15), nullable=False)
    estado = Column(String(1), nullable=False)
    fecha_insercion = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    usuario_insercion = Column(Integer, nullable=False)
    usuario_modificacion = Column(Integer, nullable=True)

    rol = relationship('Rol')

    @classmethod
    def get_by_username(cls, db_session: Session, username: str):
        return db_session.query(cls).\
            options(selectinload(cls.rol)).\
            filter_by(username=username,
                      estado=ESTADO_ACTIVO).first()
