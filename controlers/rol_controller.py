from typing import Annotated, List
from fastapi import APIRouter, Security

from models.acceso_rol import AccesoRol
from models.rol import Rol
from security.token import User
from security.utility import get_current_active_user


router = APIRouter(tags=["Roles"])

@router.post("/roles")
def create_rol(rol: Rol, current_user: Annotated[User, Security(get_current_active_user)]):
    pass

@router.post("/roles/agregarAccesos")
def add_access_to_rol(accesos_rol: List[AccesoRol], current_user: Annotated[User, Security(get_current_active_user)]):
    pass

@router.get("/roles/{rol_id}", response_model=Rol)
def read_rol(current_user: Annotated[User, Security(get_current_active_user)], rol_id: int):
    pass

@router.get("/roles", response_model=List[Rol])
def read_rols(current_user: Annotated[User, Security(get_current_active_user, scopes=["admin"])], skip: int = 0, limit: int = 10):
    pass

@router.put("/roles")
def update_rol(rol: Rol, current_user: Annotated[User, Security(get_current_active_user)]):
    pass

@router.delete("/roles/{rol_id}")
def delete_rol(rol_id: int, current_user: Annotated[User, Security(get_current_active_user)]):
    pass

@router.delete("/roles/eliminarAccesos")
def delete_access_from_rol(acceso_rol: List[AccesoRol], current_user: Annotated[User, Security(get_current_active_user)]):
    pass