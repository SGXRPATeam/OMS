from uuid import uuid4
from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.db.session import SessionLocal
from app.core.security import hash_password
from app.dtos.user_dto import (
    RegisterUserDTO,
    RegisterUserResponseDTO,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def generate_userid(db):
    row = db.execute(
        text("""
            SELECT COUNT(*) AS count
            FROM app_user
        """)
    ).fetchone()

    next_id = row.count + 1
    return f"USR{str(next_id).zfill(3)}"


@router.post(
    "/register",
    response_model=RegisterUserResponseDTO,
)
def register_user(payload: RegisterUserDTO):
    db = SessionLocal()

    try:
        email = payload.email.lower().strip()

        if "@" not in email:
            raise HTTPException(
                status_code=400,
                detail="Invalid email",
            )

        domain = email.split("@")[1]

        # find tenant
        tenant = db.execute(
            text("""
                SELECT tenantid
                FROM tenant_domain
                WHERE domain_name = :domain
                  AND status='ACTIVE'
                  AND is_deleted=FALSE
            """),
            {"domain": domain},
        ).fetchone()

        if not tenant:
            raise HTTPException(
                status_code=400,
                detail="Tenant domain not registered",
            )

        tenantid = tenant.tenantid

        # duplicate email check
        exists = db.execute(
            text("""
                SELECT userid
                FROM app_user
                WHERE email=:email
            """),
            {"email": email},
        ).fetchone()

        if exists:
            raise HTTPException(
                status_code=400,
                detail="Email already exists",
            )

        userid = generate_userid(db)

        hashed_password = hash_password(
            payload.password
        )

        # insert app_user
        db.execute(
            text("""
                INSERT INTO app_user (
                    userid,
                    tenantid,
                    username,
                    first_name,
                    last_name,
                    display_name,
                    email,
                    phone,
                    employee_code,
                    department,
                    designation,
                    role_code,
                    password_hash,
                    user_status,
                    is_mfa_enabled,
                    created_by,
                    created_date,
                    status,
                    is_deleted
                )
                VALUES (
                    :userid,
                    :tenantid,
                    :username,
                    :first_name,
                    :last_name,
                    :display_name,
                    :email,
                    :phone,
                    :employee_code,
                    :department,
                    :designation,
                    :role_code,
                    :password_hash,
                    'ACTIVE',
                    FALSE,
                    'SYSTEM',
                    NOW(),
                    'ACTIVE',
                    FALSE
                )
            """),
            {
                "userid": userid,
                "tenantid": tenantid,
                "username": email,
                "first_name": payload.first_name,
                "last_name": payload.last_name,
                "display_name": payload.display_name,
                "email": email,
                "phone": payload.phone,
                "employee_code": payload.employee_code,
                "department": payload.department,
                "designation": payload.designation,
                "role_code": payload.role_code,
                "password_hash": hashed_password,
            },
        )

        # insert mapping
        db.execute(
            text("""
                INSERT INTO user_tenant_map (
                    userid,
                    tenantid,
                    role_code,
                    access_scope,
                    is_default_tenant,
                    mapping_status,
                    created_by,
                    created_date,
                    status,
                    is_deleted
                )
                VALUES (
                    :userid,
                    :tenantid,
                    :role_code,
                    'FULL',
                    TRUE,
                    'ACTIVE',
                    'SYSTEM',
                    NOW(),
                    'ACTIVE',
                    FALSE
                )
            """),
            {
                "userid": userid,
                "tenantid": tenantid,
                "role_code": payload.role_code,
            },
        )

        db.commit()

        return RegisterUserResponseDTO(
            message="User registered successfully",
            userid=userid,
        )

    finally:
        db.close()