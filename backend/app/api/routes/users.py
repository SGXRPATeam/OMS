from fastapi import APIRouter
from sqlalchemy import text
from app.db.session import SessionLocal

router = APIRouter()


@router.get("/")
def get_all_users():
    db = SessionLocal()

    rows = db.execute(
        text("""
            SELECT
                userid,
                first_name,
                last_name,
                email,
                role_code,
                tenantid
            FROM app_user
            WHERE is_deleted = FALSE
            ORDER BY created_date DESC
        """)
    ).fetchall()

    db.close()

    data = []

    for row in rows:
        data.append({
            "userid": row.userid,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "email": row.email,
            "role_code": row.role_code,
            "tenantid": row.tenantid,
        })

    return data