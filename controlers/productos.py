from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query
from models.product import Product
from security.token import User
from security.utility import get_current_active_user

router = APIRouter()

products = [
    {
        "id":1,
        "descipcion":"Producto 1",
        "valor":54.20
    }
]

#get normal
@router.get('/productos')
def get_productos(current_user: Annotated[User, Depends(get_current_active_user)]):
    return products

#get con path param 
@router.get('/producto/{id}')
def get_producto(current_user: Annotated[User, Depends(get_current_active_user)],
                 id: int = Path(ge=0)):
    return list(filter(lambda item: item["id"]== id,products))

#get con query param 
@router.get('/producto')
def get_producto_by_valor(current_user: Annotated[User, Depends(get_current_active_user)],
                 valor: float = Query(gt=0)):
    return list(filter(lambda item: item["valor"]== valor,products))

#post con modelo
@router.post('/producto')
def post_producto(current_user: Annotated[User, Depends(get_current_active_user)],
                  producto: Product):
    products.append(producto)
    return products

#put con modelo
@router.post('/producto')
def put_producto(current_user: Annotated[User, Depends(get_current_active_user)],
                 producto: Product):
    for index, item in enumerate(products):
        if item["id"] == producto["id"]:
            products[index]["descripcion"]=producto.descripcion
            products[index]["valor"]=producto.valor
    return products     