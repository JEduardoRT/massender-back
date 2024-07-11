from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.filtro import Filtro
from config.db import get_db
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/listar-filtros")
async def listar_filtros(db: Session = Depends(get_db)):
    try:
        generos = db.query(Filtro).all()
        resultado = [{"id": genero.id, "name": genero.name, "value": genero.value} for genero in generos]
        return JSONResponse(content=resultado, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
