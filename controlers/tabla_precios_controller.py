from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from datetime import datetime

from models.tabla_precios import TablaPrecios, TablaPreciosCreate, TablaPreciosUpdate
from models.usuario import Usuario
from repository.tabla_precios import TablaPrecios as TablaPreciosRepo
from security.utility import get_current_active_user
from config.db import get_db
from utils.constants import ESTADO_ACTIVO, ESTADO_INACTIVO

router = APIRouter(tags=["TablaPrecios"])


@router.post("/tablaPrecios", response_model=TablaPrecios)
def create_tablaPrecios(
        current_user: Annotated[Usuario, Security(get_current_active_user,
                                                  scopes=["admin"])],
        tablaPrecios: TablaPreciosCreate,
        db: Session = Depends(get_db)):
    try:
        tablaPrecios.fecha_insercion = datetime.now()
        db_tablaPrecios = TablaPreciosRepo(
            cliente_id=tablaPrecios.cliente_id,
            membresia_id=tablaPrecios.membresia_id,
            fecha_tablaPrecios=tablaPrecios.fecha_tablaPrecios,
            pagado=tablaPrecios.pagado,
            cod_medio_tablaPrecios=tablaPrecios.cod_medio_tablaPrecios,
            estado=ESTADO_ACTIVO,
            fecha_insercion=tablaPrecios.fecha_insercion,
            tablaPrecios_insercion=tablaPrecios.tablaPrecios_insercion)

        db.add(db_tablaPrecios)
        db.commit()
        db.refresh(db_tablaPrecios)
        return db_tablaPrecios
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/tablaPrecios/{tabla_precios_id}", response_model=TablaPrecios)
def read_tablaPrecios(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        tabla_precios_id: int,
        db: Session = Depends(get_db)):
    try:
        tablaPrecios = db.query(TablaPreciosRepo).\
            filter(TablaPreciosRepo.tabla_precios_id == tabla_precios_id,
                   TablaPreciosRepo.estado == ESTADO_ACTIVO).\
            first()

        if not tablaPrecios:
            raise HTTPException(status_code=404,
                                detail="Tabla de Precios no encontrado")
        return tablaPrecios
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/tablaPrecios", response_model=List[TablaPrecios])
def read_tablasPrecios(current_user: Annotated[Usuario, Security(
                get_current_active_user,
                scopes=["admin"])],
               db: Session = Depends(get_db)):
    try:
        tablaPrecios = db.query(TablaPreciosRepo).\
            filter(TablaPreciosRepo.estado == ESTADO_ACTIVO).\
            all()
        return tablaPrecios
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.put("/tablaPrecios", response_model=TablaPreciosUpdate)
def update_tablaPrecios(
        current_user: Annotated[Usuario, Security(get_current_active_user,
                                                  scopes=["admin"])],
        tablaPrecios: TablaPreciosUpdate,
        db: Session = Depends(get_db)):
    try:
        tablaPrecios_existente = db.query(TablaPreciosRepo).\
            filter(
                TablaPreciosRepo.tabla_precios_id == tablaPrecios.tabla_precios_id,
                TablaPreciosRepo.estado == ESTADO_ACTIVO).\
            first()
        if not tablaPrecios_existente:
            raise HTTPException(status_code=404,
                                detail="Tabla de Precios no encontrado")

        tablaPrecios.fecha_modificacion = datetime.now()

        for key, value in tablaPrecios.model_dump(exclude_unset=True,
                                                  exclude={'tabla_precios_id',
                                                           'fecha_insercion',
                                                           'usuario_insercion',
                                                           'estado'}).items():
            setattr(tablaPrecios_existente, key, value)

        db.commit()
        db.refresh(tablaPrecios_existente)
        return tablaPrecios_existente
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tablaPrecios/{tabla_precios_id}")
def delete_tablaPrecios(
        current_user: Annotated[Usuario, Security(
            get_current_active_user,
            scopes=["admin"])],
        tabla_precios_id: int,
        db: Session = Depends(get_db)):
    try:
        tablaPrecios = db.query(TablaPreciosRepo).\
            filter(TablaPreciosRepo.tabla_precios_id == tabla_precios_id,
                   TablaPreciosRepo.estado == ESTADO_ACTIVO,
                   TablaPreciosRepo.tabla_precios_id != 1).\
            first()
        if not tablaPrecios:
            raise HTTPException(status_code=404,
                                detail="Tabla de Precios no encontrado")

        setattr(tablaPrecios, 'estado', ESTADO_INACTIVO)
        db.commit()
        return {"message": "Tabla de Precios eliminado con éxito"}
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))
