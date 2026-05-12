from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from app.schemas.product import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductResponse,
)

from app.services.product_service import (
    create_product,
    get_products,
    get_product_by_id,
    update_product,
    delete_product,
)

from app.core.security import (
    decode_access_token,
)

router = APIRouter()

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials,
):
    token = credentials.credentials

    decoded = decode_access_token(
        token
    )

    if not decoded:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    return decoded

@router.get(
    "",
    response_model=list[ProductResponse],
)
def get_all_products(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    decoded = get_current_user(credentials)

    return get_products(
        decoded["tenantid"]
    )



@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_single_product(
    product_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    decoded = get_current_user(credentials)

    product = get_product_by_id(
        decoded["tenantid"],
        product_id,
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product



@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product_api(
    product_id: str,
    payload: ProductUpdateRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    decoded = get_current_user(credentials)

    product = update_product(
        tenantid=decoded["tenantid"],
        product_id=product_id,
        payload=payload,
        updated_by=decoded["userid"],
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@router.delete(
    "/{product_id}",
)
def delete_product_api(
    product_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    decoded = get_current_user(credentials)

    return delete_product(
        tenantid=decoded["tenantid"],
        product_id=product_id,
        deleted_by=decoded["userid"],
    )


@router.post(
    "",
    response_model=ProductResponse,
)
def create_product_api(
    payload: ProductCreateRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    decoded = decode_access_token(
        token
    )

    if not decoded:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    tenantid = decoded["tenantid"]
    userid = decoded["userid"]

    result = create_product(
        tenantid=tenantid,
        payload=payload,
        created_by=userid,
    )

    return result