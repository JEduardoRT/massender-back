from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session, noload
from datetime import datetime

from models.usuario import Usuario, UsuarioCreate, UsuarioUpdate
from repository.usuario import Usuario as UsuarioRepo
from security.utility import generate_password, get_current_active_user, get_password_hash
from config.db import get_db
from services.send_email import enviar_correo
from utils.constants import ASUNTO_RECUPERAR, CORREO_RECUPERACION, ESTADO_ACTIVO, ESTADO_INACTIVO

router = APIRouter(tags=["Usuarios"])


@router.post("/usuarios", response_model=Usuario)
def create_usuario(
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
        return db_usuario
    except Exception as e:
        db.rollback()
        if type(e) is HTTPException:
            raise e
        else:
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
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/usuarios/recuperar/{correo}", response_model=int)
def recuperar_usuario(
        correo: str,
        db: Session = Depends(get_db)):
    usuario: UsuarioRepo
    password: str
    try:
        usuario = db.query(UsuarioRepo).\
            options(noload(UsuarioRepo.rol)).\
            filter(UsuarioRepo.correo == correo,
                   UsuarioRepo.estado == ESTADO_ACTIVO).\
            first()

        if not usuario:
            return 0

        password = generate_password()
        usuario.fecha_modificacion = datetime.now()
        usuario.password = get_password_hash(password)

        db.commit()
        db.refresh(usuario)
        return usuario.usuario_id
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))
    finally:
        mensaje = CORREO_RECUPERACION
        mensaje = mensaje.replace("NOMBRE", usuario.nombre_completo)
        mensaje = mensaje.replace("USUARIO", usuario.username)
        mensaje = mensaje.replace("PASSWORD", password)
        enviar_correo([usuario.correo], ASUNTO_RECUPERAR, mensaje)


@router.get("/usuarios", response_model=List[Usuario])
def read_usuarios(current_user: Annotated[Usuario, Security(
                get_current_active_user)],
              cliente_id: int = None,
              db: Session = Depends(get_db)):
    try:
        query = db.query(UsuarioRepo).\
            filter(UsuarioRepo.rol_id != 1,
                   UsuarioRepo.estado == ESTADO_ACTIVO)

        if cliente_id is not None:
            query = query.filter(UsuarioRepo.cliente_id == cliente_id)

        usuarios = query.options(noload(UsuarioRepo.rol)).\
            all()
        return usuarios
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.put("/usuarios", response_model=Usuario)
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
        if type(e) is HTTPException:
            raise e
        else:
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
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))
