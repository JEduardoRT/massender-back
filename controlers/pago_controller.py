from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from datetime import datetime

from models.pago import Pago, PagoCreate, PagoUpdate
from models.usuario import Usuario
from repository.pago import Pago as PagoRepo
from security.utility import get_current_active_user, get_password_hash
from config.db import get_db
from utils.constants import ESTADO_ACTIVO, ESTADO_INACTIVO

router = APIRouter(tags=["Pagos"])


@router.post("/pagos", response_model=PagoCreate)
def create_pago(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        pago: PagoCreate,
        db: Session = Depends(get_db)):
    try:
        pago.fecha_insercion = datetime.now()
        db_pago = PagoRepo(
            cliente_id=pago.cliente_id,
            membresia_id=pago.membresia_id,
            fecha_pago=pago.fecha_pago,
            pagado=pago.pagado,
            cod_medio_pago=pago.cod_medio_pago,
            estado=ESTADO_ACTIVO,
            fecha_insercion=pago.fecha_insercion,
            pago_insercion=pago.pago_insercion)

        db.add(db_pago)
        db.commit()
        db.refresh(db_pago)
        return pago
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pagos/{pago_id}", response_model=Pago)
def read_pago(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        pago_id: int,
        db: Session = Depends(get_db)):
    try:
        pago = db.query(PagoRepo).\
            filter(PagoRepo.pago_id == pago_id,
                   PagoRepo.estado == ESTADO_ACTIVO).\
            first()

        if not pago:
            raise HTTPException(status_code=404,
                                detail="Pago no encontrado")
        return pago
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pagos", response_model=List[Pago])
def read_pagos(current_user: Annotated[Usuario, Security(
                get_current_active_user,
                scopes=["admin"])],
               db: Session = Depends(get_db)):
    try:
        pagos = db.query(PagoRepo).\
            all()
        return pagos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pagos/bycliente/{cliente_id}", response_model=List[Pago])
def read_pagos_cliente(current_user: Annotated[Usuario, Security(
                get_current_active_user,
                scopes=["admin"])],
               cliente_id: int,
               db: Session = Depends(get_db)):
    try:
        pagos = db.query(PagoRepo).\
            filter(PagoRepo.cliente_id == cliente_id,
                   PagoRepo.estado == ESTADO_ACTIVO).\
            all()
        return pagos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/pagos", response_model=PagoUpdate)
def update_pago(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        pago: PagoUpdate,
        db: Session = Depends(get_db)):
    try:
        pago_existente = db.query(PagoRepo).\
            filter(PagoRepo.pago_id == pago.pago_id,
                   PagoRepo.estado == ESTADO_ACTIVO).\
            first()
        if not pago_existente:
            raise HTTPException(status_code=404,
                                detail="Pago no encontrado")

        pago.fecha_modificacion = datetime.now()

        for key, value in pago.model_dump(exclude_unset=True,
                                          exclude={'pago_id',
                                                   'fecha_insercion',
                                                   'usuario_insercion',
                                                   'estado',
                                                   'membresia_id',
                                                   'fecha_pago',
                                                   'cliente_id'}).items():
            if key == 'password':
                value = get_password_hash(value)
            setattr(pago_existente, key, value)

        db.commit()
        db.refresh(pago_existente)
        return pago_existente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/pagos/{pago_id}")
def delete_pago(
        current_user: Annotated[Usuario, Security(
            get_current_active_user,
            scopes=["admin"])],
        pago_id: int,
        db: Session = Depends(get_db)):
    try:
        pago = db.query(PagoRepo).\
            filter(PagoRepo.pago_id == pago_id,
                   PagoRepo.estado == ESTADO_ACTIVO).\
            first()
        if not pago:
            raise HTTPException(status_code=404,
                                detail="Pago no encontrado")

        setattr(pago, 'estado', ESTADO_INACTIVO)
        db.commit()
        return {"message": "Pago eliminado con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
