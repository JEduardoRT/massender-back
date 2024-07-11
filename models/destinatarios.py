from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CHAR, VARCHAR
from config.db import engine, Base


class Destinatario(Base):
    __tablename__ = "destinatario"
    destinatario_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(CHAR(20), nullable=False)
    apellido = Column(CHAR(20), nullable=False)
    correo = Column(VARCHAR(50), nullable=False)
    telefono = Column(VARCHAR(15), nullable=False)
    lista_id = Column(Integer, ForeignKey('lista_destinatarios.id'), nullable=False)
    estado = Column(CHAR(1), nullable=False)
    genero = Column(CHAR(1), nullable=False)
    cedula = Column(CHAR(20), nullable=False)



Base.metadata.create_all(bind=engine)
