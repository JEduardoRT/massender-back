from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from config.db import Base


class UsuarioCampania(Base):
    __tablename__ = 'UsuarioCampania'

    usuario_camp_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('Usuario.usuario_id'), nullable=False)
    campania_id = Column(Integer, ForeignKey('Campania.campania_id'), nullable=False)
    estado = Column(String(1), nullable=False)
    fecha_insercion = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    usuario_insercion = Column(Integer, nullable=False)
    usuario_modificacion = Column(Integer, nullable=True)