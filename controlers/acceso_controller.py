from typing import Annotated, List
from fastapi import APIRouter, Security

from models.acceso import Acceso
from security.token import User
from security.utility import get_current_active_user


router = APIRouter(tags=["Accesos"])

@router.post("/accesos/")
def create_acceso(acceso: Acceso, current_user: Annotated[User, Security(get_current_active_user)]):
    pass

@router.get("/accesos/{acceso_id}", response_model=Acceso)
def read_acceso(current_user: Annotated[User, Security(get_current_active_user)], acceso_id: int):
    pass

@router.get("/accesos/", response_model=List[Acceso])
def read_accesos(current_user: Annotated[User, Security(get_current_active_user)], skip: int = 0, limit: int = 10):
    pass

@router.put("/accesos/")
def update_acceso(acceso: Acceso, current_user: Annotated[User, Security(get_current_active_user)]):
    pass

@router.delete("/accesos/{acceso_id}")
def delete_acceso(acceso_id: int, current_user: Annotated[User, Security(get_current_active_user)]):
    pass