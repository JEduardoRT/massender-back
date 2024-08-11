from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from datetime import datetime

from models.membresia import Membresia, MembresiaCreate, MembresiaUpdate
from models.usuario import Usuario
from repository.membresia import Membresia as MembresiaRepo
from security.utility import get_current_active_user
from config.db import get_db
from utils.constants import ESTADO_ACTIVO, ESTADO_INACTIVO

router = APIRouter(tags=["Membresias"])


@router.post("/membresias", response_model=Membresia)
def create_membresia(
        current_user: Annotated[Usuario, Security(
             get_current_active_user,
             scopes=["admin"])],
        membresia: MembresiaCreate,
        db: Session = Depends(get_db)):
    try:
        membresia.fecha_insercion = datetime.now()
        db_membresia = MembresiaRepo(
            titulo=membresia.titulo,
            descripcion=membresia.descripcion,
            dias_vigencia=membresia.dias_vigencia,
            estado=ESTADO_ACTIVO,
            fecha_insercion=membresia.fecha_insercion,
            usuario_insercion=membresia.usuario_insercion)

        db.add(db_membresia)
        db.commit()
        db.refresh(db_membresia)
        return db_membresia
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/membresias/{membresia_id}", response_model=Membresia)
def read_membresia(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        membresia_id: int,
        db: Session = Depends(get_db)):
    try:
        membresia = db.query(MembresiaRepo).\
            filter(MembresiaRepo.membresia_id == membresia_id,
                   MembresiaRepo.estado == ESTADO_ACTIVO).\
            first()

        if not membresia:
            raise HTTPException(status_code=404,
                                detail="membresia no encontrada")
        return membresia
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/membresias", response_model=List[Membresia])
def read_membresias(current_user: Annotated[Usuario, Security(
                get_current_active_user)],
              db: Session = Depends(get_db)):
    try:
        membresias = db.query(MembresiaRepo).\
            filter(MembresiaRepo.estado == ESTADO_ACTIVO).\
            all()
        return membresias
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.put("/membresias", response_model=MembresiaUpdate)
def update_membresia(
        current_user: Annotated[Usuario, Security(get_current_active_user,
                                scopes=["admin"])],
        membresia: MembresiaUpdate,
        db: Session = Depends(get_db)):
    try:
        membresia_existente = db.query(MembresiaRepo).\
            filter(MembresiaRepo.membresia_id == membresia.membresia_id,
                   MembresiaRepo.estado == ESTADO_ACTIVO).\
            first()
        if not membresia_existente:
            raise HTTPException(status_code=404,
                                detail="membresia no encontrada")

        membresia.fecha_modificacion = datetime.now()

        for key, value in membresia.model_dump(exclude_unset=True,
                                               exclude={'membresia_id',
                                                        'fecha_insercion',
                                                        'usuario_insercion',
                                                        'estado'}).items():
            setattr(membresia_existente, key, value)

        db.commit()
        db.refresh(membresia_existente)
        return membresia_existente
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.delete("/membresias/{membresia_id}")
def delete_membresia(
        current_user: Annotated[Usuario, Security(
            get_current_active_user,
            scopes=["admin"])],
        membresia_id: int,
        db: Session = Depends(get_db)):
    try:
        membresia = db.query(MembresiaRepo).\
            filter(MembresiaRepo.membresia_id == membresia_id,
                   MembresiaRepo.estado == ESTADO_ACTIVO).\
            first()
        if not membresia:
            raise HTTPException(status_code=404,
                                detail="membresia no encontrada")

        setattr(membresia, 'estado', ESTADO_INACTIVO)
        db.commit()
        return {"message": "membresia eliminada con éxito"}
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))
