from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create_order():
    return {"message": "Order created successfully"}


@router.get("/")
def get_all_orders():
    return {"message": "Fetched all orders"}


@router.put("/{order_id}")
def update_order(order_id: str):
    return {"message": f"Order {order_id} updated successfully"}


@router.delete("/{order_id}")
def delete_order(order_id: str):
    return {"message": f"Order {order_id} deleted successfully"}