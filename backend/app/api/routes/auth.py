from fastapi import APIRouter, HTTPException, Header
from sqlalchemy import text
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import Depends

from app.db.session import SessionLocal
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    TenantInfo,
    SwitchTenantRequest,
    SwitchTenantResponse,
)
from app.core.security import (
    create_access_token,
    verify_password,
    decode_access_token,
)

router = APIRouter()
security = HTTPBearer()


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(payload: LoginRequest):
    db = SessionLocal()

    try:
        email = payload.email.strip().lower()
        password = payload.password.strip()

        if "@" not in email:
            raise HTTPException(
                status_code=400,
                detail="Invalid email format",
            )

        domain = email.split("@")[1]
        is_platform_user = (
            domain == "solugenix.com"
        )

        # resolve tenant from domain
        tenant_query = text("""
            SELECT tenantid, tenant_name
            FROM tenant
            WHERE domain_name = :domain
              AND status = 'ACTIVE'
              AND is_deleted = FALSE
        """)

        tenant_row = db.execute(
            tenant_query,
            {"domain": domain},
        ).fetchone()

        if not tenant_row and not is_platform_user:
            raise HTTPException(
                status_code=401,
                detail="Unknown tenant domain",
            )

        domain_tenantid = (
            tenant_row.tenantid
            if tenant_row
            else None
        )

        # find user
        user_query = text("""
            SELECT userid,
                   email,
                   password_hash,
                           display_name,
           first_name
            FROM app_user
            WHERE email = :email
              AND user_status = 'ACTIVE'
              AND status = 'ACTIVE'
              AND is_deleted = FALSE
        """)

        user = db.execute(
            user_query,
            {"email": email},
        ).fetchone()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found",
            )
        

        print("typed password =", password)
        print( "password check =",
    verify_password(
        password,
        user.password_hash,
    ),
)

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid password",
            )

        # mapped tenants
        mapped_query = text("""
            SELECT
                utm.tenantid,
                t.tenant_name,
                utm.role_code,
                rm.role_name
            FROM user_tenant_map utm
            JOIN tenant t
              ON t.tenantid = utm.tenantid
            JOIN role_master rm
              ON rm.role_code = utm.role_code
            WHERE utm.userid = :userid
              AND utm.mapping_status = 'ACTIVE'
              AND utm.status = 'ACTIVE'
              AND utm.is_deleted = FALSE
            ORDER BY t.tenant_name
        """)

        mapped_rows = db.execute(
            mapped_query,
            {"userid": user.userid},
        ).fetchall()

        if not mapped_rows:
            raise HTTPException(
                status_code=401,
                detail="No tenant access mapped",
            )

        tenants = [
            TenantInfo(
                tenantid=row.tenantid,
                tenant_name=row.tenant_name,
                role_code=row.role_code,
                role=row.role_name,
            )
            for row in mapped_rows
        ]

        # active tenant selection
        active = None

        if is_platform_user:
            active = mapped_rows[0]
        else:
            for row in mapped_rows:
                if row.tenantid == domain_tenantid:
                    active = row
                    break

            if not active:
                raise HTTPException(
                    status_code=401,
                    detail="Domain tenant not mapped",
                )

        # create token
        token = create_access_token(
            {
                "userid": user.userid,
                "email": user.email,
                "tenantid": active.tenantid,
                "role": active.role_name,
            }
        )

        return LoginResponse(
          access_token=token,
          token_type="bearer",
          userid=user.userid,
          tenantid=active.tenantid,
          role=active.role_name,
          email=user.email,
          display_name=(
            user.display_name
            or user.first_name
            or user.email
    ),
    tenants=tenants,
)

    finally:
        db.close()

@router.post(
    "/switch-tenant",
    response_model=SwitchTenantResponse,
)
def switch_tenant(
    payload: SwitchTenantRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    db = SessionLocal()

    try:
        token = credentials.credentials

        decoded = decode_access_token(
            token
        )

        if not decoded:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )

        userid = decoded["userid"]

        tenant_query = text("""
            SELECT
                utm.tenantid,
                utm.role_code,
                rm.role_name
            FROM user_tenant_map utm
            JOIN role_master rm
              ON rm.role_code = utm.role_code
            WHERE utm.userid = :userid
              AND utm.tenantid = :tenantid
              AND utm.mapping_status = 'ACTIVE'
              AND utm.status = 'ACTIVE'
              AND utm.is_deleted = FALSE
        """)

        row = db.execute(
            tenant_query,
            {
                "userid": userid,
                "tenantid": payload.tenantid,
            },
        ).fetchone()

        if not row:
            raise HTTPException(
                status_code=403,
                detail="Tenant access denied",
            )

        new_token = create_access_token(
            {
                "userid": userid,
                "email": decoded["email"],
                "tenantid": row.tenantid,
                "role": row.role_name,
            }
        )

        return SwitchTenantResponse(
            access_token=new_token,
            token_type="bearer",
            tenantid=row.tenantid,
            role=row.role_name,
        )

    finally:
        db.close()