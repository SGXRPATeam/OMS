from fastapi import APIRouter

from app.api.routes import auth
from app.api.routes import users
from app.api.routes import orders
from app.api.routes import non_orders
from app.api.routes import dashboard

api_router = APIRouter()


# Authentication
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

# Users
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

# Orders
api_router.include_router(
    orders.router,
    prefix="/orders",
    tags=["Orders"],
)

# Non Orders
api_router.include_router(
    non_orders.router,
    prefix="/non-orders",
    tags=["Non Orders"],
)

# Dashboard
api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"],
)