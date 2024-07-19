from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from models.lista_destinatarios import ListaDestinatarios
from models.destinatarios import Destinatario
from config.db import get_db
from models.lista_destinatarios_request import ListaDestinatariosRequest
from security.token import User
from security.utility import get_current_active_user

router = APIRouter()

@router.post("/guardar-destinatarios")
async def guardar_destinatarios(current_user: Annotated[User, Security(get_current_active_user)], data: ListaDestinatariosRequest, db: Session = Depends(get_db)):
    try:
        # Crear la lista de destinatarios
        nueva_lista = ListaDestinatarios(
            nombre=data.nombreLista,
            estado='A',
            fecha_modificacion=datetime.utcnow()
        )
        db.add(nueva_lista)
        db.commit()
        db.refresh(nueva_lista)

        # Crear los destinatarios
        for dest in data.destinatarios:
            nuevo_destinatario = Destinatario(
                cedula=dest.cedula,
                nombre=dest.nombre,
                apellido=dest.apellido,
                correo=dest.correo,
                telefono=dest.telefono,
                genero=dest.genero,
                lista_id=nueva_lista.id,
                estado='A'
            )
            db.add(nuevo_destinatario)
        db.commit()

        return JSONResponse(content={"message": "Lista de contactos creada con éxito."}, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/listar-destinatarios")
async def listar_destinatarios(current_user: Annotated[User, Security(get_current_active_user)], db: Session = Depends(get_db)):
    try:
        listas = db.query(ListaDestinatarios).filter_by(estado='A').all()
        resultado = []
        for lista in listas:
            destinatarios = db.query(Destinatario).filter_by(lista_id=lista.id, estado='A').all()
            resultado.append({
                "id": lista.id,
                "nombre": lista.nombre,
                "fecha_modificacion": lista.fecha_modificacion.isoformat(),  # Convertimos la fecha a un formato serializable
                "destinatarios": [
                    {
                        "cedula": dest.cedula,
                        "nombre": dest.nombre,
                        "apellido": dest.apellido,
                        "correo": dest.correo,
                        "telefono": dest.telefono,
                        "genero": dest.genero
                    } for dest in destinatarios
                ]
            })
        return JSONResponse(content=resultado, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/verdestinatarioporlista/{lista_id}")
async def verdestinatarioporlista(current_user: Annotated[User, Security(get_current_active_user)], lista_id: int, db: Session = Depends(get_db)):
    try:
        destinatarios = db.query(Destinatario).filter(Destinatario.lista_id == lista_id, Destinatario.estado == 'A').all()
        if not destinatarios:
            raise HTTPException(status_code=404, detail="No se encontraron destinatarios para la lista especificada")
        return destinatarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))