from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from datetime import datetime
from models.acceso import Acceso, AccesoCreate, AccesoUpdate
from models.usuario import Usuario
from repository.rol import Rol as RolRepo
from repository.acceso import Acceso as AccesoRepo
from repository.acceso_rol import AccesoRol as AccesoRolRepo
from security.utility import get_current_active_user
from config.db import get_db
from utils.constants import ESTADO_ACTIVO, ESTADO_INACTIVO

router = APIRouter(tags=["Accesos"])


@router.post("/accesos", response_model=AccesoCreate)
def create_acceso(
            current_user: Annotated[Usuario, Security(
                get_current_active_user,
                scopes=["admin"])],
            acceso: AccesoCreate,
            db: Session = Depends(get_db)):
    try:
        acceso.fecha_insercion = datetime.now()
        db_acceso = AccesoRepo(
            ruta=acceso.ruta,
            descripcion=acceso.descripcion,
            estado=ESTADO_ACTIVO,
            fecha_insercion=acceso.fecha_insercion,
            usuario_insercion=acceso.usuario_insercion,
            parent_id=acceso.parent_id)

        db.add(db_acceso)
        db.commit()
        db.refresh(db_acceso)
        return acceso
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/accesos/{acceso_id}", response_model=Acceso)
def read_acceso(
            current_user: Annotated[Usuario, Security(get_current_active_user)],
            acceso_id: int,
            db: Session = Depends(get_db)):
    try:
        acceso = db.query(AccesoRepo).\
            filter(AccesoRepo.acceso_id == acceso_id,
                   AccesoRepo.estado == ESTADO_ACTIVO).\
            first()

        if not acceso:
            raise HTTPException(status_code=404, detail="Acceso no encontrado")
        return acceso

    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/accesos", response_model=List[Acceso])
def read_accesos(
            current_user: Annotated[Usuario, Security(
                get_current_active_user,
                scopes=["admin"])],
            db: Session = Depends(get_db)):
    try:
        accesos = db.query(AccesoRepo).\
            filter(AccesoRepo.estado == ESTADO_ACTIVO).\
            all()
        return accesos
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/accesos/byrol/{rol_id}", response_model=List[Acceso])
def read_accesos_by_rol(
            current_user: Annotated[Usuario, Security(get_current_active_user)],
            rol_id: int,
            db: Session = Depends(get_db)):

    try:
        accesos = db.query(AccesoRepo).\
            join(AccesoRolRepo).\
            filter(AccesoRolRepo.rol_id == rol_id,
                   AccesoRepo.estado == ESTADO_ACTIVO).\
            all()

        accesosModel: List[Acceso] = []
        for acceso in accesos:
            accesoModel = Acceso(
                acceso_id=acceso.acceso_id,
                ruta=acceso.ruta,
                descripcion=acceso.descripcion,
                parent_id=acceso.parent_id,
                estado=acceso.estado,
                fecha_insercion=acceso.fecha_insercion,
                usuario_insercion=acceso.usuario_insercion,
                fecha_modificacion=acceso.fecha_modificacion,
                usuario_modificacion=acceso.usuario_modificacion
            )
            accesosModel.append(accesoModel)

        accesos_dict = {acceso.acceso_id: acceso for acceso in accesosModel}

        for acceso in accesos:
            if acceso.parent_id is not None and acceso.parent_id in accesos_dict:
                parent = accesos_dict[acceso.parent_id]
                if parent.children is None:
                    parent.children = []
                parent.children.append(acceso)

        accesos_filtrados = [acceso for acceso in accesosModel if acceso.parent_id is None]

        return accesos_filtrados
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.put("/accesos", response_model=AccesoUpdate)
def update_acceso(
            current_user: Annotated[Usuario, Security(
                get_current_active_user,
                scopes=["admin"])],
            acceso: AccesoUpdate,
            db: Session = Depends(get_db)):
    try:
        acceso_existente = db.query(AccesoRepo).\
            filter(AccesoRepo.acceso_id == acceso.acceso_id,
                   AccesoRepo.estado == ESTADO_ACTIVO).\
            first()
        if not acceso_existente:
            raise HTTPException(status_code=404, detail="Acceso no encontrado")

        acceso.fecha_modificacion = datetime.now()

        for key, value in acceso.model_dump(exclude_unset=True,
                                            exclude={'acceso_id',
                                                     'fecha_insercion',
                                                     'usuario_insercion',
                                                     'estado'}).\
                items():
            setattr(acceso_existente, key, value)

        db.commit()
        db.refresh(acceso_existente)
        return acceso
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.delete("/accesos/{acceso_id}")
def delete_acceso(
            current_user: Annotated[Usuario, Security(
                get_current_active_user,
                scopes=["admin"])],
            acceso_id: int,
            db: Session = Depends(get_db)):
    try:
        acceso = db.query(AccesoRepo).\
            filter(AccesoRepo.acceso_id == acceso_id,
                   AccesoRepo.estado == ESTADO_ACTIVO).\
            first()
        if not acceso:
            raise HTTPException(status_code=404, detail="Acceso no encontrado")

        setattr(acceso, 'estado', ESTADO_INACTIVO)
        db.commit()
        return {"message": "Acceso eliminado con éxito"}
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))
