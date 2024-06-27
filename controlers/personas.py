from fastapi import APIRouter
from config.db import conn
from models.persona import personas, Persona
from typing import List

router = APIRouter()

@router.get('/personas', response_model=List[Persona])
def get_personas():
    result = conn.execute(personas.select()).fetchall()
    personas_list = [dict(row._mapping) for row in result]
    return personas_list

@router.post('/personas')
def create_personas(pers: Persona):
    print(conn.execute(personas.select()).lastrowid())
    new_persona = {"nombre": pers.nombre, "edad": pers.edad, "correo": pers.correo}
    result = conn.execute(personas.insert().values(new_persona))
    conn.commit()
    return conn.execute(personas.select().where(personas.c.id == result.lastrowid)).first()