from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.db.session import SessionLocal
from app.schemas.auth import LoginRequest, LoginResponse
from app.core.security import create_access_token, verify_password

router = APIRouter()


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

        tenant_query = text("""
            SELECT tenantid
            FROM tenant_domain
            WHERE domain_name = :domain
              AND status = 'ACTIVE'
              AND is_deleted = FALSE
        """)

        tenant_row = db.execute(
            tenant_query,
            {"domain": domain},
        ).fetchone()

        if not tenant_row:
            raise HTTPException(
                status_code=401,
                detail="Unknown tenant domain",
            )

        tenantid = tenant_row.tenantid

        user_query = text("""
            SELECT userid,
                   email,
                   password_hash,
                   role_code,
                   tenantid
            FROM app_user
            WHERE email = :email
              AND tenantid = :tenantid
              AND status = 'ACTIVE'
              AND is_deleted = FALSE
        """)

        user = db.execute(
            user_query,
            {
                "email": email,
                "tenantid": tenantid,
            },
        ).fetchone()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid password",
            )

        role_query = text("""
            SELECT role_name
            FROM role_master
            WHERE role_code = :role_code
        """)

        role = db.execute(
            role_query,
            {"role_code": user.role_code},
        ).fetchone()

        if not role:
            raise HTTPException(
                status_code=401,
                detail="Role not found",
            )

        token = create_access_token(
            {
                "userid": user.userid,
                "email": user.email,
                "tenantid": user.tenantid,
                "role": role.role_name,
            }
        )

        return LoginResponse(
            access_token=token,
            token_type="bearer",
            userid=user.userid,
            tenantid=user.tenantid,
            role=role.role_name,
            email=user.email,
        )

    finally:
        db.close()