
from datetime import datetime
from models.base import MassenderBase


class AccesoRol(MassenderBase):
    acceso_id: int
    rol_id: int


class AccesoRolCreate(AccesoRol):
    fecha_insercion: datetime
    usuario_insercion: int


class AccesoRolUpdate(AccesoRol):
    fecha_modificacion: datetime
    usuario_modificacion: int
