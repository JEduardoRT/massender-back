from fastapi import FastAPI

app = FastAPI()

products = [
    {
        "id":1,
        "descipcion":"Producto 1",
        "valor":54.20
    }
]

#get normal
@app.get('/productos')
def message():
    return products

#get con path param 
@app.get('/producto/{id}')
def get_producto(id: int):
    return list(filter(lambda item: item["id"]== id,products))


#get con query param 
@app.get('/producto')
def get_producto(valor: float):
    return list(filter(lambda item: item["valor"]== valor,products))