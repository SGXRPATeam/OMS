from fastapi import APIRouter
from app.api.routes import auth, users, products, orders, cases, inquiries

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(cases.router, prefix="/cases", tags=["Cases"])
api_router.include_router(inquiries.router, prefix="/inquiries", tags=["Inquiries"])