from fastapi import FastAPI
import uvicorn
from controlers.acceso_controller import router as AccesoController
from controlers.security import router as SecurityController

app = FastAPI(root_path="/massender")

app.include_router(AccesoController)
app.include_router(SecurityController)

#this is for DEBUG (comment when launch in prod)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)