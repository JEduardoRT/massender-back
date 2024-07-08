from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from models.lista_destinatarios import ListaDestinatarios
from models.destinatarios import Destinatario
from config.db import get_db
from models.lista_destinatarios_request import ListaDestinatariosRequest

router = APIRouter()

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

        return JSONResponse(content={"message": "Lista de contactos creada con éxito."}, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
