from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_product():
    return {"message": "Create Product"}

@router.get("/")
def get_products():
    return {"message": "Get All Products"}

@router.get("/{product_id}")
def get_product(product_id: str):
    return {"message": f"Get Product {product_id}"}

@router.put("/{product_id}")
def update_product(product_id: str):
    return {"message": f"Update Product {product_id}"}

@router.delete("/{product_id}")
def delete_product(product_id: str):
    return {"message": f"Delete Product {product_id}"}