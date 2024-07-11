from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base

class Filtro(Base):
    __tablename__ = 'filtros'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    name = Column(String, index=True)
    value = Column(String, index=True)

    campanias = relationship("Campania", back_populates="filtro")