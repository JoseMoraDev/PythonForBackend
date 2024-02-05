from fastapi import APIRouter



router = APIRouter(
    prefix="/products", 
    tags=["products"], # creates a new section in the documentation
    responses={404: {"message": "Not found"}}
)



producs_list = ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]



# @router.get("/products") deprecated because I'm using prefix "/products"
@router.get("/") # same as "/products"
async def products():
    return producs_list



# @router.get("/products/{id}") deprecated 
@router.get("/{id}") # same as "/products/{id}"
async def products(id: int):
    return producs_list[id]