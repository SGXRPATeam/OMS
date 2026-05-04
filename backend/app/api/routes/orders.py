from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from app.db.session import SessionLocal
from app.dtos.order_dto import OrderCreateDTO, OrderUpdateDTO
from datetime import datetime, timedelta

router = APIRouter()


def generate_case_id(db):
    row = db.execute(
        text("""
            SELECT COUNT(*) FROM oms_case
            WHERE case_type='ORDER'
        """)
    ).scalar()

    return f"CAS{str(row + 1).zfill(3)}"


@router.post("/")
def create_order(payload: OrderCreateDTO):
    db = SessionLocal()

    delivery_date = datetime.utcnow() + timedelta(days=5)

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
             due_date,
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
                'ORDER',
                :case_category,
                'MEDIUM',
                'NORMAL',
                'OPEN',
                :value,
                'USD',
                :external_case_id,
                :resolution_summary,
:due_date,
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
            "case_category": payload.order_type,
            "value": payload.quantity,
            "external_case_id": payload.account_number,
            "resolution_summary": payload.delivery_address,
"due_date": delivery_date,
"created_date": datetime.utcnow(),
            "updated_date": datetime.utcnow(),
        },
    )

    db.commit()
    db.close()

    return {
        "message": "Order created successfully",
        "caseid": caseid,
    }


@router.get("/")
def get_orders():
    db = SessionLocal()

    rows = db.execute(
        text("""
            SELECT
                caseid,
                external_case_id,
                case_subject,
                value,
                case_details,
                resolution_summary,
                case_category,
case_status,
due_date,
created_date
            FROM oms_case
            WHERE case_type='ORDER'
            AND is_deleted=FALSE
            ORDER BY created_date DESC
        """)
    ).fetchall()

    db.close()

    return [
        {
            "caseid": row.caseid,
            "account_number": row.external_case_id,
            "product": row.case_subject,
            "quantity": row.value,
            "description": row.case_details,
            "delivery_address": row.resolution_summary,
           "order_type": row.case_category,
"status": row.case_status,
"delivery_date": row.due_date,
"created_date": row.created_date,
        }
        for row in rows
    ]


@router.put("/{caseid}")
def update_order(caseid: str, payload: OrderUpdateDTO):
    db = SessionLocal()

    db.execute(
        text("""
            UPDATE oms_case
            SET
                external_case_id=:external_case_id,
                case_subject=:case_subject,
                value=:value,
                case_details=:case_details,
                resolution_summary=:resolution_summary,
                case_category=:case_category,
                updated_date=:updated_date
            WHERE caseid=:caseid
        """),
        {
            "caseid": caseid,
            "external_case_id": payload.account_number,
            "case_subject": payload.product,
            "value": payload.quantity,
            "case_details": payload.description,
            "resolution_summary": payload.delivery_address,
            "case_category": payload.order_type,
            "updated_date": datetime.utcnow(),
        },
    )

    db.commit()
    db.close()

    return {"message": "Order updated successfully"}


@router.delete("/{caseid}")
def delete_order(caseid: str):
    db = SessionLocal()

    db.execute(
        text("""
            UPDATE oms_case
            SET is_deleted=TRUE
            WHERE caseid=:caseid
        """),
        {"caseid": caseid},
    )

    db.commit()
    db.close()

    return {"message": "Order deleted successfully"}