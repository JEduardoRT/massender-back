from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base

class Campania(Base):
    __tablename__ = 'campania_list'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255))
    mensaje = Column(Text)
    filtro_id = Column(Integer, ForeignKey('filtros.id'))
    lista_id = Column(Integer, ForeignKey('lista_destinatarios.id'))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    estado = Column(String(50), default='A')

    # Relaciones
    filtro = relationship("Filtro", back_populates="campanias")
    lista = relationship("ListaDestinatarios", back_populates="campanias")
