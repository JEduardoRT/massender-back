from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from datetime import datetime

from models.acceso_rol import AccesoRol, AccesoRolCreate
from models.rol import Rol, RolCreate, RolUpdate
from models.usuario import Usuario
from repository.rol import Rol as RolRepo
from repository.acceso_rol import AccesoRol as AccesoRolRepo
from security.utility import get_current_active_user
from config.db import get_db
from utils.constants import ESTADO_ACTIVO, ESTADO_INACTIVO

router = APIRouter(tags=["Roles"])


@router.post("/roles", response_model=RolCreate)
def create_rol(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        rol: RolCreate,
        db: Session = Depends(get_db)):
    try:
        rol.fecha_insercion = datetime.now()
        db_rol = RolRepo(
            scopes='user',
            descripcion=rol.descripcion,
            estado=ESTADO_ACTIVO,
            fecha_insercion=rol.fecha_insercion,
            usuario_insercion=rol.usuario_insercion)

        db.add(db_rol)
        db.commit()
        db.refresh(db_rol)
        return rol
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/roles/agregarAccesos")
def add_access_to_rol(current_user: Annotated[Usuario, Security(get_current_active_user)],
                      accesos_rol: List[AccesoRolCreate],
                      db: Session = Depends(get_db)):
    try:
        for acceso_rol in accesos_rol:
            acceso_rol.fecha_insercion = datetime.now()
            acceso_rol.estado = ESTADO_ACTIVO

            db_acceso_rol = AccesoRolRepo(
                acceso_id=acceso_rol.acceso_id,
                rol_id=acceso_rol.rol_id,
                estado=ESTADO_ACTIVO,
                fecha_insercion=acceso_rol.fecha_insercion,
                usuario_insercion=acceso_rol.usuario_insercion)
            db.add(db_acceso_rol)
        db.commit()
        return {"message": "Accesos agregados al rol con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/roles/{rol_id}", response_model=Rol)
def read_rol(current_user: Annotated[Usuario, Security(get_current_active_user)],
             rol_id: int,
             db: Session = Depends(get_db)):
    try:
        rol = db.query(RolRepo).\
            filter(RolRepo.rol_id == rol_id,
                   RolRepo.estado == ESTADO_ACTIVO).\
            first()

        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return rol
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/roles", response_model=List[Rol])
def read_rols(current_user: Annotated[Usuario, Security(
                get_current_active_user,
                scopes=["admin"])],
              db: Session = Depends(get_db)):
    try:
        roles = db.query(RolRepo).\
            all()
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/roles", response_model=RolUpdate)
def update_rol(current_user: Annotated[Usuario, Security(get_current_active_user)],
               rol: RolUpdate,
               db: Session = Depends(get_db)):
    try:
        rol_existente = db.query(RolRepo).\
            filter(RolRepo.rol_id == rol.rol_id,
                   RolRepo.estado == ESTADO_ACTIVO).\
            first()
        if not rol_existente:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        rol.fecha_modificacion = datetime.now()

        for key, value in rol.model_dump(exclude_unset=True,
                                         exclude={'rol_id',
                                                  'fecha_insercion',
                                                  'usuario_insercion',
                                                  'estado',
                                                  'scopes'}).items():
            setattr(rol_existente, key, value)

        db.commit()
        db.refresh(rol_existente)
        return rol_existente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/roles/{rol_id}")
def delete_rol(current_user: Annotated[Usuario, Security(get_current_active_user)],
               rol_id: int,
               db: Session = Depends(get_db)):
    try:
        rol = db.query(RolRepo).\
            filter(RolRepo.rol_id == rol_id,
                   RolRepo.estado == ESTADO_ACTIVO).\
            first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        setattr(rol, 'estado', ESTADO_INACTIVO)
        db.commit()
        return {"message": "Rol eliminado con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/roles/eliminarAccesos")
def delete_access_from_rol(current_user: Annotated[Usuario, Security(get_current_active_user)],
                           accesos_rol: List[AccesoRol],
                           db: Session = Depends(get_db)):
    try:
        for acceso_rol in accesos_rol:
            acceso_rol_existente = db.query(AccesoRolRepo).\
                filter(
                    AccesoRolRepo.acceso_id == acceso_rol.acceso_id,
                    AccesoRolRepo.rol_id == acceso_rol.rol_id
                ).\
                first()
            if acceso_rol_existente:
                db.delete(acceso_rol_existente)
        db.commit()
        return {"message": "Accesos eliminados del rol con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
