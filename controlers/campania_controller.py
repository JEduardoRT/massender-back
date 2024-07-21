from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
import logging

from starlette.responses import JSONResponse

from models.destinatarios import Destinatario
from models.filtro import Filtro
from models.campania import Campania
from config.db import get_db
from pydantic import BaseModel
from typing import List, Optional

from models.lista_destinatarios import ListaDestinatarios
from services.send_email import enviar_correo

router = APIRouter(tags=["Campañas"])

# Configurar el registro
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Esquemas de Pydantic
class CampaniaCreate(BaseModel):
    nombre: str
    mensaje: str
    filtro_id: Optional[int]
    lista_id: int


class CampaniaResponse(BaseModel):
    id: int
    nombre: str
    mensaje: str
    filtro_id: int
    lista_id: Optional[int]
    lista_nombre: str
    fecha_creacion: datetime
    estado: str

    class Config:
        from_attributes = True


@router.post("/guardar-campania", response_model=CampaniaResponse)
async def guardar_campania(campania: CampaniaCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Guardando campaña: {campania.nombre}")

        nueva_campania = Campania(
            nombre=campania.nombre,
            mensaje=campania.mensaje,
            filtro_id=campania.filtro_id,
            lista_id=campania.lista_id,
            fecha_creacion=datetime.utcnow(),
            estado='A'
        )
        db.add(nueva_campania)
        db.commit()
        db.refresh(nueva_campania)

        logger.info(f"Campaña guardada con ID: {nueva_campania.id}")

        filtro = db.query(Filtro).filter(Filtro.id == campania.filtro_id).first()
        if campania.filtro_id and not filtro:
            raise HTTPException(status_code=400, detail="Filtro no encontrado")

        if campania.filtro_id and filtro.value != "N":
            destinatarios = db.query(Destinatario).filter_by(lista_id=campania.lista_id, genero=filtro.value).all()
        else:
            destinatarios = db.query(Destinatario).filter(Destinatario.lista_id == campania.lista_id).all()

        if not destinatarios:
            raise HTTPException(status_code=404, detail="No se encontraron destinatarios para la campaña")

        email_list = [destinatario.correo for destinatario in destinatarios]
        logger.info(f"Enviando correos a: {email_list}")

        enviar_correo(email_list, campania.nombre, campania.mensaje)
        logger.info("Correos enviados con éxito")

        lista = db.query(ListaDestinatarios).filter(ListaDestinatarios.id == campania.lista_id).first()
        lista_nombre = lista.nombre if lista else "N/A"

        return CampaniaResponse(
            id=nueva_campania.id,
            nombre=nueva_campania.nombre,
            mensaje=nueva_campania.mensaje,
            filtro_id=nueva_campania.filtro_id,
            lista_id=nueva_campania.lista_id,
            lista_nombre=lista_nombre,
            fecha_creacion=nueva_campania.fecha_creacion,
            estado=nueva_campania.estado
        )

    except Exception as e:
        logger.error(f"Error al guardar la campaña: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/listar-campanias", response_model=List[CampaniaResponse])
async def listar_campanias(db: Session = Depends(get_db)):
    try:
        campanias = (
            db.query(Campania)
            .options(joinedload(Campania.lista))
            .all()
        )

        resultado = []
        for campania in campanias:
            logger.info(f"Procesando campaña: {campania.nombre}")
            resultado.append({
                "id": campania.id,
                "nombre": campania.nombre,
                "mensaje": campania.mensaje,
                "filtro_id": campania.filtro_id,
                "lista_id": campania.lista_id,
                "lista_nombre": campania.lista.nombre if campania.lista else "N/A",  # Manejar NoneType
                "fecha_creacion": campania.fecha_creacion,
                "estado": campania.estado,
            })

        logger.info("Listar campañas completado con éxito")
        return resultado
    except Exception as e:
        logger.error(f"Error al listar campañas: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/eliminar-campania/{campania_id}")
async def eliminar_campania(campania_id: int, db: Session = Depends(get_db)):
    try:
        # Buscar la campaña por ID
        campania = db.query(Campania).filter(Campania.id == campania_id).first()
        if not campania:
            raise HTTPException(status_code=404, detail="Campaña no encontrada")

        # Eliminar la campaña
        db.delete(campania)
        db.commit()

        return JSONResponse(
            content={"message": "Campaña eliminada con éxito."},
            status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
