from typing import Annotated, List
from fastapi import APIRouter, Security

from models.campania import Campania
from security.token import User
from security.utility import get_current_active_user


router = APIRouter(tags=["Campañas"])

@router.post("/campanias/")
def create_campania(campania: Campania, current_user: Annotated[User, Security(get_current_active_user)]):
    pass

@router.get("/campanias/{campania_id}", response_model=Campania)
def read_campania(current_user: Annotated[User, Security(get_current_active_user)], campania_id: int):
    pass

@router.get("/campanias/", response_model=List[Campania])
def read_campanias(current_user: Annotated[User, Security(get_current_active_user)], skip: int = 0, limit: int = 10):
    pass

@router.put("/campanias/")
def update_campania(campania: Campania, current_user: Annotated[User, Security(get_current_active_user)]):
    pass

@router.delete("/campanias/{campania_id}")
def delete_campania(campania_id: int, current_user: Annotated[User, Security(get_current_active_user)]):
    pass