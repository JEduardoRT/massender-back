from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from datetime import datetime

from models.acceso_rol import AccesoRol
from models.rol import Rol
from security.token import User
from security.utility import get_current_active_user
from config.db import get_db

router = APIRouter(tags=["Roles"])

@router.post("/roles", response_model=Rol)
def create_rol(current_user: Annotated[User, Security(get_current_active_user)], rol: Rol, db: Session = Depends(get_db)):
    try:
        rol.fecha_insercion = datetime.utcnow()
        rol.usuario_insercion = current_user.id
        db.add(rol)
        db.commit()
        db.refresh(rol)
        return rol
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/roles/agregarAccesos")
def add_access_to_rol(current_user: Annotated[User, Security(get_current_active_user)], accesos_rol: List[AccesoRol], db: Session = Depends(get_db)):
    try:
        for acceso_rol in accesos_rol:
            acceso_rol.fecha_insercion = datetime.utcnow()
            acceso_rol.usuario_insercion = current_user.id
            db.add(acceso_rol)
        db.commit()
        return {"message": "Accesos agregados al rol con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/roles/{rol_id}", response_model=Rol)
def read_rol(current_user: Annotated[User, Security(get_current_active_user)], rol_id: int, db: Session = Depends(get_db)):
    try:
        rol = db.query(Rol).filter(Rol.rol_id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return rol
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/roles", response_model=List[Rol])
def read_rols(current_user: Annotated[User, Security(get_current_active_user, scopes=["admin"])], skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        roles = db.query(Rol).offset(skip).limit(limit).all()
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/roles", response_model=Rol)
def update_rol(current_user: Annotated[User, Security(get_current_active_user)], rol: Rol, db: Session = Depends(get_db)):
    try:
        rol_existente = db.query(Rol).filter(Rol.rol_id == rol.rol_id).first()
        if not rol_existente:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        rol.fecha_modificacion = datetime.utcnow()
        rol.usuario_modificacion = current_user.id

        for key, value in rol.dict().items():
            setattr(rol_existente, key, value)

        db.commit()
        db.refresh(rol_existente)
        return rol_existente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/roles/{rol_id}")
def delete_rol(current_user: Annotated[User, Security(get_current_active_user)], rol_id: int, db: Session = Depends(get_db)):
    try:
        rol = db.query(Rol).filter(Rol.rol_id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        db.delete(rol)
        db.commit()
        return {"message": "Rol eliminado con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/roles/eliminarAccesos")
def delete_access_from_rol(current_user: Annotated[User, Security(get_current_active_user)], accesos_rol: List[AccesoRol], db: Session = Depends(get_db)):
    try:
        for acceso_rol in accesos_rol:
            acceso_rol_existente = db.query(AccesoRol).filter(
                AccesoRol.acceso_id == acceso_rol.acceso_id,
                AccesoRol.rol_id == acceso_rol.rol_id
            ).first()
            if acceso_rol_existente:
                db.delete(acceso_rol_existente)
        db.commit()
        return {"message": "Accesos eliminados del rol con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
