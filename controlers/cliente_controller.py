from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from datetime import datetime

from models.cliente import Cliente, ClienteCreate, ClienteUpdate
from models.usuario import Usuario
from repository.cliente import Cliente as ClienteRepo
from security.utility import get_current_active_user
from config.db import get_db
from utils.constants import ESTADO_ACTIVO, ESTADO_INACTIVO

router = APIRouter(tags=["Clientes"])


@router.post("/clientes", response_model=Cliente)
def create_cliente(
        cliente: ClienteCreate,
        db: Session = Depends(get_db)):
    try:
        cliente.fecha_insercion = datetime.now()
        db_cliente = ClienteRepo(
            nombre=cliente.nombre,
            membresia_id=cliente.membresia_id,
            tabla_precios_id=cliente.tabla_precios_id,
            medio_pago_id=cliente.medio_pago_id,
            fecha_ini_memb=cliente.fecha_ini_memb,
            fecha_fin_memb=cliente.fecha_fin_memb,
            estado=ESTADO_ACTIVO,
            fecha_insercion=cliente.fecha_insercion,
            usuario_insercion=cliente.usuario_insercion)

        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/clientes/{cliente_id}", response_model=Cliente)
def read_cliente(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        cliente_id: int,
        db: Session = Depends(get_db)):
    try:
        cliente = db.query(ClienteRepo).\
            filter(ClienteRepo.cliente_id == cliente_id,
                   ClienteRepo.estado == ESTADO_ACTIVO).\
            first()

        if not cliente:
            raise HTTPException(status_code=404,
                                detail="Cliente no encontrado")
        return cliente
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/clientes", response_model=List[Cliente])
def read_clientes(current_user: Annotated[Usuario, Security(
                get_current_active_user,
                scopes=["admin"])],
              db: Session = Depends(get_db)):
    try:
        clientes = db.query(ClienteRepo).\
            filter(ClienteRepo.estado == ESTADO_ACTIVO).\
            all()
        return clientes
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.put("/clientes", response_model=Cliente)
def update_cliente(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        cliente: ClienteUpdate,
        db: Session = Depends(get_db)):
    try:
        cliente_existente = db.query(ClienteRepo).\
            filter(ClienteRepo.cliente_id == cliente.cliente_id,
                   ClienteRepo.estado == ESTADO_ACTIVO).\
            first()
        if not cliente_existente:
            raise HTTPException(status_code=404,
                                detail="Cliente no encontrado")

        cliente.fecha_modificacion = datetime.now()

        for key, value in cliente.model_dump(exclude_unset=True,
                                             exclude={'cliente_id',
                                                      'fecha_insercion',
                                                      'usuario_insercion',
                                                      'estado'}).items():
            setattr(cliente_existente, key, value)

        db.commit()
        db.refresh(cliente_existente)
        return cliente_existente
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clientes/{cliente_id}")
def delete_cliente(
        current_user: Annotated[Usuario, Security(
            get_current_active_user,
            scopes=["admin"])],
        cliente_id: int,
        db: Session = Depends(get_db)):
    try:
        cliente = db.query(ClienteRepo).\
            filter(ClienteRepo.cliente_id == cliente_id,
                   ClienteRepo.estado == ESTADO_ACTIVO).\
            first()
        if not cliente:
            raise HTTPException(status_code=404,
                                detail="Cliente no encontrado")

        setattr(cliente, 'estado', ESTADO_INACTIVO)
        db.commit()
        return {"message": "Cliente eliminado con éxito"}
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))
