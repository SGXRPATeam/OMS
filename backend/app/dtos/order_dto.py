from pydantic import BaseModel


class OrderCreateDTO(BaseModel):
    account_number: str
    product: str
    quantity: float
    description: str
    delivery_address: str
    order_type: str


class OrderUpdateDTO(BaseModel):
    account_number: str
    product: str
    quantity: float
    description: str
    delivery_address: str
    order_type: str