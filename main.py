from fastapi import FastAPI
from controlers.productos import router as ProductController

app = FastAPI()
app.include_router(ProductController)