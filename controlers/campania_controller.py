from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from models.lista_destinatarios import ListaDestinatarios
from repository.destinatarios import Destinatario
from models.filtro import Filtro
from models.campania import Campania
from config.db import get_db
from pydantic import BaseModel
from typing import List, Optional

from services.send_email import enviar_correo

router = APIRouter()


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
    lista_id: int
    fecha_creacion: datetime
    estado: str

    class Config:
        from_attributes = True


@router.post("/guardar-campania", response_model=CampaniaResponse)
async def guardar_campania(campania: CampaniaCreate, db: Session = Depends(get_db)):
    try:
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

        filtro = db.query(Filtro).filter(Filtro.id == campania.filtro_id).first()
        if not filtro:
            raise HTTPException(status_code=400, detail="Filtro no encontrado")
        if filtro.value != "N":
            destinatarios = db.query(Destinatario).filter_by(lista_id=campania.lista_id, genero=filtro.value).all()
        else:
            destinatarios = db.query(Destinatario).filter(lista_id=campania.lista_id).all()

        email_list = [destinatario.correo for destinatario in destinatarios]

        print(email_list)

        enviar_correo(email_list, campania.nombre, campania.mensaje)
        return nueva_campania

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/listar-campanias", response_model=List[CampaniaResponse])
async def listar_campanias(db: Session = Depends(get_db)):
    try:
        campanias = db.query(Campania).filter_by(estado='A').all()
        return campanias
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
