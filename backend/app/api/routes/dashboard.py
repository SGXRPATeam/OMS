from fastapi import APIRouter
from sqlalchemy import text
from app.db.session import SessionLocal

router = APIRouter()


@router.get("/stats")
def get_dashboard_stats():
    db = SessionLocal()

    total_orders = db.execute(
        text("SELECT COUNT(*) FROM oms_order WHERE is_deleted=FALSE")
    ).scalar()

    delayed_orders = db.execute(
        text("""
            SELECT COUNT(*)
            FROM oms_order
            WHERE order_status='DELAYED'
            AND is_deleted=FALSE
        """)
    ).scalar()

    total_inquiries = db.execute(
        text("SELECT COUNT(*) FROM inquiry WHERE is_deleted=FALSE")
    ).scalar()

    db.close()

    return {
        "total_orders": total_orders,
        "active_orders": total_orders - delayed_orders,
        "delayed_orders": delayed_orders,
        "total_inquiries": total_inquiries,
        "in_progress": 63,
        "pending": 18,
    }