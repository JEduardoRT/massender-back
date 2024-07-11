from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CHAR, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy.orm import relationship

from config.db import engine, Base


class ListaDestinatarios(Base):
    __tablename__ = "lista_destinatarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(CHAR(50), nullable=False)
    estado = Column(CHAR(1), nullable=False)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)

    # Relación inversa
    campanias = relationship("Campania", back_populates="lista")
