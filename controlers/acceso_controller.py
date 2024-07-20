from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from datetime import datetime

from models.acceso import Acceso
from security.token import User
from security.utility import get_current_active_user
from config.db import get_db

router = APIRouter(tags=["Accesos"])


@router.post("/accesos", response_model=Acceso)
def create_acceso(current_user: Annotated[User, Security(get_current_active_user)], acceso: Acceso, db: Session = Depends(get_db)):
    try:
        acceso.fecha_insercion = datetime.utcnow()
        acceso.usuario_insercion = current_user.id
        db.add(acceso)
        db.commit()
        db.refresh(acceso)
        return acceso
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/accesos/{acceso_id}", response_model=Acceso)
def read_acceso(current_user: Annotated[User, Security(get_current_active_user)], acceso_id: int, db: Session = Depends(get_db)):
    try:
        acceso = db.query(Acceso).filter(Acceso.acceso_id == acceso_id).first()
        if not acceso:
            raise HTTPException(status_code=404, detail="Acceso no encontrado")
        return acceso
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/accesos", response_model=List[Acceso])
def read_accesos(current_user: Annotated[User, Security(get_current_active_user, scopes=["admin"])], db: Session = Depends(get_db)):
    try:
        accesos = db.query(Acceso).all()
        return accesos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/accesos/byrol/{rol_id}", response_model=List[Acceso])
def read_accesos_by_rol(current_user: Annotated[User, Security(get_current_active_user)], rol_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        accesos = db.query(Acceso).filter(Acceso.rol_id == rol_id).offset(skip).limit(limit).all()
        return accesos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/accesos", response_model=Acceso)
def update_acceso(current_user: Annotated[User, Security(get_current_active_user)], acceso: Acceso, db: Session = Depends(get_db)):
    try:
        acceso_existente = db.query(Acceso).filter(Acceso.acceso_id == acceso.acceso_id).first()
        if not acceso_existente:
            raise HTTPException(status_code=404, detail="Acceso no encontrado")

        acceso.fecha_modificacion = datetime.utcnow()
        acceso.usuario_modificacion = current_user.id

        for key, value in acceso.dict().items():
            setattr(acceso_existente, key, value)

        db.commit()
        db.refresh(acceso_existente)
        return acceso_existente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/accesos/{acceso_id}")
def delete_acceso(current_user: Annotated[User, Security(get_current_active_user)], acceso_id: int, db: Session = Depends(get_db)):
    try:
        acceso = db.query(Acceso).filter(Acceso.acceso_id == acceso_id).first()
        if not acceso:
            raise HTTPException(status_code=404, detail="Acceso no encontrado")

        db.delete(acceso)
        db.commit()
        return {"message": "Acceso eliminado con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
