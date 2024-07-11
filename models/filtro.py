from sqlalchemy import Column, Integer, String
from config.db import Base


class Filters(Base):
    __tablename__ = "filtros"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False)
    value = Column(String(45), nullable=False)
