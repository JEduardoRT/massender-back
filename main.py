from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from controlers.acceso_controller import router as acceso_controller
from controlers.security import router as security_controller
from controlers.destinatarios_controller import router as destinatarios_controller
from controlers.dictionaries_controller import router as dictionaries_controller
from controlers.campania_controller import router as campania_controller


app = FastAPI(root_path="/massender")

# Configuración de CORS
origins = [
    "http://localhost",  # Si tu aplicación Angular se ejecuta en localhost
    "http://localhost:4200",  # Ajusta el puerto según sea necesario
    # Añade otros orígenes según sea necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(acceso_controller)
app.include_router(security_controller)
app.include_router(destinatarios_controller)
app.include_router(dictionaries_controller)
app.include_router(campania_controller)

# this is for DEBUG (comment when launch in prod)
#if __name__ == "__main__":
#    uvicorn.run(app, host="localhost", port=8000)
