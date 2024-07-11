from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from models.lista_destinatarios import ListaDestinatarios
from models.destinatarios import Destinatario
from models.filtro import Filtro
from models.campania import Campania
from config.db import get_db
from pydantic import BaseModel
from typing import List, Optional

from services.send_email import send_email

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
        orm_mode = True


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

        destinatarios = db.query(Destinatario).filter_by(lista_id=campania.lista_id).all()
        email_list = [destinatario.correo for destinatario in destinatarios]

        send_email(email_list, campania.nombre, campania.mensaje)
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
