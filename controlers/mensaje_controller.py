from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from datetime import datetime

from models.mensaje import Mensaje, MensajeCreate, MensajeUpdate
from models.usuario import Usuario
from repository.mensaje import Mensaje as MensajeRepo
from security.utility import get_current_active_user
from config.db import get_db
from utils.constants import ESTADO_ACTIVO, ESTADO_INACTIVO

router = APIRouter(tags=["Mensajes"])


@router.post("/mensajes", response_model=MensajeCreate)
def create_mensaje(
        current_user: Annotated[Usuario, Security(
             get_current_active_user,
             scopes=["admin"])],
        mensaje: MensajeCreate,
        db: Session = Depends(get_db)):
    try:
        mensaje.fecha_insercion = datetime.now()
        db_mensaje = MensajeRepo(
            campania_id=mensaje.campania_id,
            texto=mensaje.texto,
            multimedia=mensaje.multimedia,
            estado=ESTADO_ACTIVO,
            fecha_insercion=mensaje.fecha_insercion,
            usuario_insercion=mensaje.usuario_insercion)

        db.add(db_mensaje)
        db.commit()
        db.refresh(db_mensaje)
        return mensaje
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mensajes/{mensaje_id}", response_model=Mensaje)
def read_mensaje(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        mensaje_id: int,
        db: Session = Depends(get_db)):
    try:
        mensaje = db.query(MensajeRepo).\
            filter(MensajeRepo.mensaje_id == mensaje_id,
                   MensajeRepo.estado == ESTADO_ACTIVO).\
            first()

        if not mensaje:
            raise HTTPException(status_code=404,
                                detail="mensaje no encontrado")
        return mensaje
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mensajes", response_model=List[Mensaje])
def read_mensajes(current_user: Annotated[Usuario, Security(
                get_current_active_user,
                scopes=["admin"])],
              db: Session = Depends(get_db)):
    try:
        mensajes = db.query(MensajeRepo).\
            all()
        return mensajes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/mensajes", response_model=MensajeUpdate)
def update_mensaje(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        mensaje: MensajeUpdate,
        db: Session = Depends(get_db)):
    try:
        mensaje_existente = db.query(MensajeRepo).\
            filter(MensajeRepo.mensaje_id == mensaje.mensaje_id,
                   MensajeRepo.estado == ESTADO_ACTIVO).\
            first()
        if not mensaje_existente:
            raise HTTPException(status_code=404,
                                detail="mensaje no encontrado")

        mensaje.fecha_modificacion = datetime.now()

        for key, value in mensaje.model_dump(exclude_unset=True,
                                             exclude={'mensaje_id',
                                                      'campania_id',
                                                      'fecha_insercion',
                                                      'usuario_insercion',
                                                      'estado'}).items():
            setattr(mensaje_existente, key, value)

        db.commit()
        db.refresh(mensaje_existente)
        return mensaje_existente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/mensajes/{mensaje_id}")
def delete_mensaje(
        current_user: Annotated[Usuario, Security(
            get_current_active_user,
            scopes=["admin"])],
        mensaje_id: int,
        db: Session = Depends(get_db)):
    try:
        mensaje = db.query(MensajeRepo).\
            filter(MensajeRepo.mensaje_id == mensaje_id,
                   MensajeRepo.estado == ESTADO_ACTIVO).\
            first()
        if not mensaje:
            raise HTTPException(status_code=404,
                                detail="mensaje no encontrado")

        setattr(mensaje, 'estado', ESTADO_INACTIVO)
        db.commit()
        return {"message": "mensaje eliminado con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
