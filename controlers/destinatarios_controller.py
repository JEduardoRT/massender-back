from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime

from models.destinatario_request import DestinatarioRequest
from models.lista_destinatarios import ListaDestinatarios
from models.destinatarios import Destinatario
from config.db import get_db
from models.lista_destinatarios_request import ListaDestinatariosRequest
from models.campania import Campania
import logging


router = APIRouter(tags=["Destinatarios"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/guardar-destinatarios")
async def guardar_destinatarios(data: ListaDestinatariosRequest, db: Session = Depends(get_db)):
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

        return JSONResponse(
            content={"message": "Lista de contactos creada con éxito."},
            status_code=201)

    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/listar-destinatarios")
async def listar_destinatarios(db: Session = Depends(get_db)):
    try:
        listas = db.query(ListaDestinatarios).all()  # Obtener todas las listas, sin filtrar por estado
        resultado = []
        for lista in listas:
            destinatarios = db.query(Destinatario).filter_by(lista_id=lista.id).all()
            resultado.append({
                "id": lista.id,
                "nombre": lista.nombre,
                "fecha_modificacion": lista.fecha_modificacion.isoformat(),
                "estado": lista.estado,
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
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/verdestinatarioporlista/{lista_id}")
async def verdestinatarioporlista(
        lista_id: int, db: Session = Depends(get_db)):
    try:
        destinatarios = db.query(Destinatario).filter(Destinatario.lista_id == lista_id).all()
        if not destinatarios:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron destinatarios para la lista especificada")
        return destinatarios
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.put("/desactivar-lista/{lista_id}")
async def desactivar_lista(
    lista_id: int, db: Session = Depends(get_db)):
    try:
        # Buscar la lista de destinatarios por ID
        lista = db.query(ListaDestinatarios).filter(ListaDestinatarios.id == lista_id, ListaDestinatarios.estado == 'A').first()
        if not lista:
            raise HTTPException(status_code=404, detail="Lista no encontrada")

        # Marcar la lista y sus destinatarios asociados como inactivos
        lista.estado = 'I'
        lista.fecha_modificacion = datetime.utcnow()
        destinatarios = db.query(Destinatario).filter(Destinatario.lista_id == lista.id, Destinatario.estado == 'A').all()
        for dest in destinatarios:
            dest.estado = 'I'

        db.commit()

        return JSONResponse(
            content={"message": "Lista de contactos desactivada con éxito."},
            status_code=200)
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))

@router.put("/activar-lista/{lista_id}")
async def activar_lista(lista_id: int, db: Session = Depends(get_db)):
    try:
        # Buscar la lista de destinatarios por ID
        lista = db.query(ListaDestinatarios).filter(ListaDestinatarios.id == lista_id, ListaDestinatarios.estado == 'I').first()
        if not lista:
            raise HTTPException(status_code=404, detail="Lista no encontrada o ya está activa")

        # Marcar la lista y sus destinatarios asociados como activos
        lista.estado = 'A'
        lista.fecha_modificacion = datetime.utcnow()
        destinatarios = db.query(Destinatario).filter(Destinatario.lista_id == lista.id, Destinatario.estado == 'I').all()
        for dest in destinatarios:
            dest.estado = 'A'

        db.commit()

        return JSONResponse(
            content={"message": "Lista de contactos activada con éxito."},
            status_code=200)
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.delete("/eliminar-lista/{lista_id}")
async def eliminar_lista(lista_id: int, db: Session = Depends(get_db)):
    try:
        # Buscar la lista de destinatarios por ID
        lista = db.query(ListaDestinatarios).filter(ListaDestinatarios.id == lista_id).first()
        if not lista:
            raise HTTPException(status_code=404, detail="Lista no encontrada")

        # Eliminar las campañas asociadas a la lista
        db.query(Campania).filter(Campania.lista_id == lista_id).delete()

        # Eliminar los destinatarios asociados a la lista
        db.query(Destinatario).filter(Destinatario.lista_id == lista_id).delete()

        # Eliminar la lista de destinatarios
        db.delete(lista)
        db.commit()

        return JSONResponse(
            content={"message": "Lista de contactos y campañas asociadas eliminadas con éxito."},
            status_code=200)
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))

@router.delete("/eliminardestinatario/{id}")
async def eliminar_destinatario(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Intentando eliminar destinatario con id: {id}")
        destinatario = db.query(Destinatario).filter(Destinatario.destinatario_id == id).first()
        if not destinatario:
            logger.warning(f"Destinatario con id {id} no encontrado")
            raise HTTPException(status_code=404, detail="Destinatario no encontrado")

        db.delete(destinatario)
        db.commit()
        logger.info(f"Destinatario con id {id} eliminado con éxito")

        return JSONResponse(
            content={"message": "Destinatario eliminado con éxito."},
            status_code=200
        )
    except Exception as e:
        logger.error(f"Error al eliminar destinatario: {str(e)}")
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.put("/actualizardestinatario/{destinatario_id}")
async def actualizar_destinatario(destinatario_id: int, destinatario: DestinatarioRequest, db: Session = Depends(get_db)):
    try:
        destinatario_db = db.query(Destinatario).filter(Destinatario.destinatario_id == destinatario_id).first()
        if not destinatario_db:
            raise HTTPException(status_code=404, detail="Destinatario no encontrado")

        # Actualizar los campos del destinatario
        destinatario_db.nombre = destinatario.nombre
        destinatario_db.apellido = destinatario.apellido
        destinatario_db.correo = destinatario.correo
        destinatario_db.telefono = destinatario.telefono
        destinatario_db.genero = destinatario.genero

        db.commit()

        return JSONResponse(
            content={"message": "Destinatario actualizado con éxito."},
            status_code=200
        )
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))