from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from config.db import Base


class Cliente(Base):
    __tablename__ = 'Cliente'

    cliente_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(20), nullable=False)
    membresia_id = Column(Integer, ForeignKey('Membresia.membresia_id'), nullable=False)
    tabla_precios_id = Column(Integer, ForeignKey('TablaPrecios.tabla_precios_id'), nullable=False)
    medio_pago_id = Column(Integer, ForeignKey('MedioPago.medio_pago_id'), nullable=False)
    fecha_ini_memb = Column(Date, nullable=True)
    fecha_fin_memb = Column(Date, nullable=True)
    estado = Column(String(1), nullable=False)
    fecha_insercion = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    usuario_insercion = Column(Integer, nullable=False)
    usuario_modificacion = Column(Integer, nullable=True)