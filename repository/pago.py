from sqlalchemy import VARCHAR, Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from config.db import Base


class Pago(Base):
    __tablename__ = 'Pago'

    pago_id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('Cliente.cliente_id'), nullable=False)
    membresia_id = Column(Integer, ForeignKey('Membresia.membresia_id'), nullable=False)
    fecha_pago = Column(Date, nullable=False)
    pagado = Column(Boolean, nullable=False)
    cod_medio_pago = Column(VARCHAR(3), nullable=False)
    estado = Column(String(1), nullable=False)
    fecha_insercion = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    usuario_insercion = Column(Integer, nullable=False)
    usuario_modificacion = Column(Integer, nullable=True)