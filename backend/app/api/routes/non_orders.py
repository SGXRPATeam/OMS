from fastapi import APIRouter
from sqlalchemy import text
from app.db.session import SessionLocal
from app.dtos.order_dto import OrderCreateDTO
from datetime import datetime

router = APIRouter()


def generate_case_id(db):
    row = db.execute(
        text("SELECT COUNT(*) FROM oms_case")
    ).scalar()

    return f"CAS{str(row + 1).zfill(3)}"


@router.post("/")
def create_non_order(payload: OrderCreateDTO):
    db = SessionLocal()

    caseid = generate_case_id(db)

    db.execute(
        text("""
            INSERT INTO oms_case(
                caseid,
                tenantid,
                case_subject,
                case_details,
                case_type,
                case_category,
                priority,
                severity,
                case_status,
                value,
                currency,
                external_case_id,
                resolution_summary,
                version_no,
                created_by,
                created_date,
                updated_by,
                updated_date,
                status,
                is_deleted
            )
            VALUES(
                :caseid,
                'TEN001',
                :case_subject,
                :case_details,
                'NON_ORDER',
                'NON_ORDER',
                'MEDIUM',
                'NORMAL',
                'OPEN',
                :value,
                'USD',
                :external_case_id,
                :resolution_summary,
                1,
                'SYSTEM',
                :created_date,
                'SYSTEM',
                :updated_date,
                'ACTIVE',
                FALSE
            )
        """),
        {
            "caseid": caseid,
            "case_subject": payload.product,
            "case_details": payload.description,
            "value": payload.quantity,
            "external_case_id": payload.account_number,
            "resolution_summary": payload.delivery_address,
            "created_date": datetime.utcnow(),
            "updated_date": datetime.utcnow(),
        },
    )

    db.commit()
    db.close()

    return {
        "message": "Non Order created successfully",
        "caseid": caseid,
    }


@router.get("/")
def get_non_orders():
    db = SessionLocal()

    rows = db.execute(
        text("""
            SELECT *
            FROM oms_case
            WHERE case_type='NON_ORDER'
            AND is_deleted=FALSE
            ORDER BY created_date DESC
        """)
    ).fetchall()

    db.close()

    return [dict(row._mapping) for row in rows]