from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from controlers.acceso_controller import router as AccesoController
from controlers.security import router as SecurityController
from controlers.destinatarios_controller import router as DestinatariosController


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

app.include_router(AccesoController)
app.include_router(SecurityController)
app.include_router(DestinatariosController)

# this is for DEBUG (comment when launch in prod)
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
