from fastapi import APIRouter, Path, Query
from models.product import Product

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
def message():
    return products

#get con path param 
@router.get('/producto/{id}')
def get_producto(id: int = Path(ge=0)):
    return list(filter(lambda item: item["id"]== id,products))

#get con query param 
@router.get('/producto')
def get_producto(valor: float = Query(gt=0)):
    return list(filter(lambda item: item["valor"]== valor,products))

#post con modelo
@router.post('/producto')
def post_producto(producto: Product):
    products.append(producto)
    return products

#put con modelo
@router.post('/producto')
def put_producto(producto: Product):
    for index, item in enumerate(products):
        if item["id"] == producto["id"]:
            products[index]["descripcion"]=producto.descripcion
            products[index]["valor"]=producto.valor
    return products     