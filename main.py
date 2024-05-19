from fastapi import FastAPI
from controlers.productos import router as ProductController
from controlers.security import router as SecurityController

app = FastAPI()
app.include_router(ProductController)
app.include_router(SecurityController)