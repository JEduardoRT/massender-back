from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from datetime import datetime

from models.precio import Precio, PrecioCreate, PrecioUpdate
from models.usuario import Usuario
from repository.precio import Precio as PrecioRepo
from security.utility import get_current_active_user
from config.db import get_db
from utils.constants import ESTADO_ACTIVO, ESTADO_INACTIVO

router = APIRouter(tags=["Precios"])


@router.post("/precios", response_model=PrecioCreate)
def create_precio(
        current_user: Annotated[Usuario, Security(
             get_current_active_user,
             scopes=["admin"])],
        precio: PrecioCreate,
        db: Session = Depends(get_db)):
    try:
        precio.fecha_insercion = datetime.now()
        db_precio = PrecioRepo(
            membresia_id=precio.membresia_id,
            tabla_precios_id=precio.tabla_precios_id,
            valor=precio.valor,
            estado=ESTADO_ACTIVO,
            fecha_insercion=precio.fecha_insercion,
            usuario_insercion=precio.usuario_insercion)

        db.add(db_precio)
        db.commit()
        db.refresh(db_precio)
        return precio
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/precios/{precio_id}", response_model=Precio)
def read_precio(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        precio_id: int,
        db: Session = Depends(get_db)):
    try:
        precio = db.query(PrecioRepo).\
            filter(PrecioRepo.precio_id == precio_id,
                   PrecioRepo.estado == ESTADO_ACTIVO).\
            first()

        if not precio:
            raise HTTPException(status_code=404,
                                detail="Precio no encontrado")
        return precio
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/precios", response_model=List[Precio])
def read_precios(current_user: Annotated[Usuario, Security(
                get_current_active_user,
                scopes=["admin"])],
              db: Session = Depends(get_db)):
    try:
        precios = db.query(PrecioRepo).\
            all()
        return precios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/precios", response_model=PrecioUpdate)
def update_precio(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        precio: PrecioUpdate,
        db: Session = Depends(get_db)):
    try:
        precio_existente = db.query(PrecioRepo).\
            filter(PrecioRepo.precio_id == precio.precio_id,
                   PrecioRepo.estado == ESTADO_ACTIVO).\
            first()
        if not precio_existente:
            raise HTTPException(status_code=404,
                                detail="Precio no encontrado")

        precio.fecha_modificacion = datetime.now()

        for key, value in precio.model_dump(exclude_unset=True,
                                            exclude={'precio_id',
                                                     'membresia_id',
                                                     'tabla_precios_id',
                                                     'fecha_insercion',
                                                     'usuario_insercion',
                                                     'estado'}).items():
            setattr(precio_existente, key, value)

        db.commit()
        db.refresh(precio_existente)
        return precio_existente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/precios/{precio_id}")
def delete_precio(
        current_user: Annotated[Usuario, Security(
            get_current_active_user,
            scopes=["admin"])],
        precio_id: int,
        db: Session = Depends(get_db)):
    try:
        precio = db.query(PrecioRepo).\
            filter(PrecioRepo.precio_id == precio_id,
                   PrecioRepo.estado == ESTADO_ACTIVO).\
            first()
        if not precio:
            raise HTTPException(status_code=404,
                                detail="Precio no encontrado")

        setattr(precio, 'estado', ESTADO_INACTIVO)
        db.commit()
        return {"message": "Precio eliminado con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
