from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session, noload
from datetime import datetime

from models.usuario import Usuario, UsuarioCreate, UsuarioUpdate
from repository.usuario import Usuario as UsuarioRepo
from security.utility import get_current_active_user, get_password_hash
from config.db import get_db
from utils.constants import ESTADO_ACTIVO, ESTADO_INACTIVO

router = APIRouter(tags=["Usuarios"])


@router.post("/usuarios", response_model=UsuarioCreate)
def create_usuario(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        usuario: UsuarioCreate,
        db: Session = Depends(get_db)):
    try:
        usuario.fecha_insercion = datetime.now()
        db_usuario = UsuarioRepo(
            username=usuario.username,
            nombre_completo=usuario.nombre_completo,
            password=get_password_hash(usuario.password),
            correo=usuario.correo,
            rol_id=usuario.rol_id,
            cliente_id=usuario.cliente_id,
            telefono=usuario.telefono,
            estado=ESTADO_ACTIVO,
            fecha_insercion=usuario.fecha_insercion,
            usuario_insercion=usuario.usuario_insercion)

        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return usuario
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usuarios/{usuario_id}", response_model=Usuario)
def read_usuario(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        usuario_id: int,
        db: Session = Depends(get_db)):
    try:
        usuario = db.query(UsuarioRepo).\
            options(noload(UsuarioRepo.rol)).\
            filter(UsuarioRepo.usuario_id == usuario_id,
                   UsuarioRepo.estado == ESTADO_ACTIVO).\
            first()

        if not usuario:
            raise HTTPException(status_code=404,
                                detail="Usuario no encontrado")
        return usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usuarios", response_model=List[Usuario])
def read_usuarios(current_user: Annotated[Usuario, Security(
                get_current_active_user,
                scopes=["admin"])],
              db: Session = Depends(get_db)):
    try:
        usuarios = db.query(UsuarioRepo).\
            options(noload(UsuarioRepo.rol)).\
            all()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/usuarios", response_model=UsuarioUpdate)
def update_usuario(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        usuario: UsuarioUpdate,
        db: Session = Depends(get_db)):
    try:
        usuario_existente = db.query(UsuarioRepo).\
            options(noload(UsuarioRepo.rol)).\
            filter(UsuarioRepo.usuario_id == usuario.usuario_id,
                   UsuarioRepo.estado == ESTADO_ACTIVO).\
            first()
        if not usuario_existente:
            raise HTTPException(status_code=404,
                                detail="Usuario no encontrado")

        usuario.fecha_modificacion = datetime.now()

        for key, value in usuario.model_dump(exclude_unset=True,
                                             exclude={'usuario_id',
                                                      'fecha_insercion',
                                                      'usuario_insercion',
                                                      'estado',
                                                      'rol',
                                                      'username',
                                                      'cliente_id'}).items():
            if key == 'password':
                value = get_password_hash(value)
            setattr(usuario_existente, key, value)

        db.commit()
        db.refresh(usuario_existente)
        return usuario_existente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/usuarios/{usuario_id}")
def delete_usuario(
        current_user: Annotated[Usuario, Security(get_current_active_user)],
        usuario_id: int,
        db: Session = Depends(get_db)):
    try:
        usuario = db.query(UsuarioRepo).\
            options(noload(UsuarioRepo.rol)).\
            filter(UsuarioRepo.usuario_id == usuario_id,
                   UsuarioRepo.estado == ESTADO_ACTIVO).\
            first()
        if not usuario:
            raise HTTPException(status_code=404,
                                detail="Usuario no encontrado")

        setattr(usuario, 'estado', ESTADO_INACTIVO)
        db.commit()
        return {"message": "Usuario eliminado con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
