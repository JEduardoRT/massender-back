from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, Integer, String, Text
from config.db import Base


class Mensaje(Base):
    __tablename__ = 'Mensaje'

    mensaje_id = Column(Integer, primary_key=True, autoincrement=True)
    campania_id = Column(Integer, ForeignKey('Campania.campania_id'), nullable=False)
    texto = Column(Text, nullable=False)
    multimedia = Column(VARCHAR(2000), nullable=False)
    estado = Column(String(1), nullable=False)
    fecha_insercion = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    usuario_insercion = Column(Integer, nullable=False)
    usuario_modificacion = Column(Integer, nullable=True)
