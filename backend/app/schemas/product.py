from pydantic import BaseModel
from typing import Optional


class ProductCreateRequest(BaseModel):
    product_name: str
    product_type: str
    product_category: str
    product_sub_category: Optional[str] = None
    description: Optional[str] = None
    unit_price: float
    stock_qty: int
    uom: str
    sku_code: Optional[str] = None
    currency: Optional[str] = "INR"
    is_subscription_product: Optional[bool] = False
    tax_code: Optional[str] = None
    image_url: Optional[str] = None


class ProductUpdateRequest(BaseModel):
    product_name: str
    product_type: str
    product_category: str
    product_sub_category: Optional[str] = None
    description: Optional[str] = None
    unit_price: float
    stock_qty: int
    uom: str
    sku_code: Optional[str] = None
    currency: Optional[str] = "INR"
    is_subscription_product: Optional[bool] = False
    tax_code: Optional[str] = None
    image_url: Optional[str] = None

class ProductResponse(BaseModel):
    product_id: str
    tenantid: str
    product_code: str
    product_name: str
    product_type: str
    product_category: str
    product_sub_category: Optional[str]
    description: Optional[str]
    unit_price: float
    currency: str
    sku_code: Optional[str]
    stock_qty: int
    uom: str
    image_url: Optional[str]
    product_status: str