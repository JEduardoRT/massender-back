from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from datetime import datetime

from models.medio_pago import MedioPago, MedioPagoCreate, MedioPagoUpdate
from models.usuario import Usuario
from repository.medio_pago import MedioPago as MedioPagoRepo
from security.utility import get_current_active_user
from config.db import get_db
from utils.constants import ESTADO_ACTIVO, ESTADO_INACTIVO

router = APIRouter(tags=["MedioPagos"])


@router.post("/medioPagos", response_model=MedioPago)
def create_medioPago(
        current_user: Annotated[Usuario, Security(
             get_current_active_user,
             scopes=["admin"])],
        medioPago: MedioPagoCreate,
        db: Session = Depends(get_db)):
    try:
        medioPago.fecha_insercion = datetime.now()
        db_medioPago = MedioPagoRepo(
            descripcion=medioPago.descripcion,
            codigo=medioPago.codigo,
            estado=ESTADO_ACTIVO,
            fecha_insercion=medioPago.fecha_insercion,
            usuario_insercion=medioPago.usuario_insercion)

        db.add(db_medioPago)
        db.commit()
        db.refresh(db_medioPago)
        return db_medioPago
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/medioPagos/{medioPago_id}", response_model=MedioPago)
def read_medioPago(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        medioPago_id: int,
        db: Session = Depends(get_db)):
    try:
        medioPago = db.query(MedioPagoRepo).\
            filter(MedioPagoRepo.medio_pago_id == medioPago_id,
                   MedioPagoRepo.estado == ESTADO_ACTIVO).\
            first()

        if not medioPago:
            raise HTTPException(status_code=404,
                                detail="medio de pago no encontrado")
        return medioPago
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/medioPagos", response_model=List[MedioPago])
def read_medioPagos(current_user: Annotated[Usuario, Security(
                get_current_active_user)],
              db: Session = Depends(get_db)):
    try:
        medioPagos = db.query(MedioPagoRepo).\
            filter(MedioPagoRepo.estado == ESTADO_ACTIVO).\
            all()
        return medioPagos
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.put("/medioPagos", response_model=MedioPagoUpdate)
def update_medioPago(
        current_user: Annotated[Usuario, Security(get_current_active_user,
                                scopes=["admin"])],
        medioPago: MedioPagoUpdate,
        db: Session = Depends(get_db)):
    try:
        medioPago_existente = db.query(MedioPagoRepo).\
            filter(MedioPagoRepo.medio_pago_id == medioPago.medio_pago_id,
                   MedioPagoRepo.estado == ESTADO_ACTIVO).\
            first()
        if not medioPago_existente:
            raise HTTPException(status_code=404,
                                detail="medio de pago no encontrado")

        medioPago.fecha_modificacion = datetime.now()

        for key, value in medioPago.model_dump(exclude_unset=True,
                                               exclude={'medio_pago_id',
                                                        'fecha_insercion',
                                                        'usuario_insercion',
                                                        'estado'}).items():
            setattr(medioPago_existente, key, value)

        db.commit()
        db.refresh(medioPago_existente)
        return medioPago_existente
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.delete("/medioPagos/{medioPago_id}")
def delete_medioPago(
        current_user: Annotated[Usuario, Security(
            get_current_active_user,
            scopes=["admin"])],
        medioPago_id: int,
        db: Session = Depends(get_db)):
    try:
        medioPago = db.query(MedioPagoRepo).\
            filter(MedioPagoRepo.medio_pago_id == medioPago_id,
                   MedioPagoRepo.estado == ESTADO_ACTIVO).\
            first()
        if not medioPago:
            raise HTTPException(status_code=404,
                                detail="medio de pago no encontrado")

        setattr(medioPago, 'estado', ESTADO_INACTIVO)
        db.commit()
        return {"message": "medio de pago eliminado con éxito"}
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))
