from sqlalchemy import text
from app.db.session import SessionLocal


def generate_product_code(db):
    query = text("""
        SELECT COUNT(*) AS total
        FROM product
    """)

    count = db.execute(query).fetchone()

    next_no = (count.total or 0) + 1

    return f"PRD{next_no:04d}"


def create_product(
    tenantid: str,
    payload,
    created_by: str,
):
    db = SessionLocal()

    try:
        product_id = generate_product_code(db)

        product_code = product_id

        query = text("""
            INSERT INTO product (
                product_id,
                tenantid,
                product_code,
                product_name,
                product_type,
                product_category,
                product_sub_category,
                description,
                unit_price,
                currency,
                sku_code,
                stock_qty,
                uom,
                image_url,
                product_status,
                is_subscription_product,
                tax_code,
                version_no,
                created_by,
                created_date,
                updated_by,
                updated_date,
                status,
                is_deleted
            )
            VALUES (
                :product_id,
                :tenantid,
                :product_code,
                :product_name,
                :product_type,
                :product_category,
                :product_sub_category,
                :description,
                :unit_price,
                :currency,
                :sku_code,
                :stock_qty,
                :uom,
                :image_url,
                'ACTIVE',
                :is_subscription_product,
                :tax_code,
                1,
                :created_by,
                NOW(),
                :updated_by,
                NOW(),
                'ACTIVE',
                FALSE
            )
        """)

        db.execute(
            query,
            {
                "product_id": product_id,
                "tenantid": tenantid,
                "product_code": product_code,
                "product_name": payload.product_name,
                "product_type": payload.product_type,
                "product_category": payload.product_category,
                "product_sub_category": payload.product_sub_category,
                "description": payload.description,
                "unit_price": payload.unit_price,
                "currency": payload.currency,
                "sku_code": payload.sku_code,
                "stock_qty": payload.stock_qty,
                "uom": payload.uom,
                "image_url": payload.image_url,
                "is_subscription_product": payload.is_subscription_product,
                "tax_code": payload.tax_code,
                "created_by": created_by,
                "updated_by": created_by,
            },
        )

        db.commit()

        return {
            "product_id": product_id,
            "tenantid": tenantid,
            "product_code": product_code,
            "product_name": payload.product_name,
            "product_type": payload.product_type,
            "product_category": payload.product_category,
            "product_sub_category": payload.product_sub_category,
            "description": payload.description,
            "unit_price": payload.unit_price,
            "currency": payload.currency,
            "sku_code": payload.sku_code,
            "stock_qty": payload.stock_qty,
            "uom": payload.uom,
            "image_url": payload.image_url,
            "product_status": "ACTIVE",
        }
    
    

    finally:
        db.close()

def get_products(tenantid: str):
    db = SessionLocal()

    try:
        query = text("""
            SELECT
                product_id,
                tenantid,
                product_code,
                product_name,
                product_type,
                product_category,
                product_sub_category,
                description,
                unit_price,
                currency,
                sku_code,
                stock_qty,
                uom,
                image_url,
                product_status
            FROM product
            WHERE tenantid = :tenantid
              AND is_deleted = FALSE
              AND status = 'ACTIVE'
            ORDER BY created_date DESC
        """)

        rows = db.execute(
            query,
            {"tenantid": tenantid},
        ).fetchall()

        return [dict(row._mapping) for row in rows]

    finally:
        db.close()


def get_product_by_id(
    tenantid: str,
    product_id: str,
):
    db = SessionLocal()

    try:
        query = text("""
            SELECT
                product_id,
                tenantid,
                product_code,
                product_name,
                product_type,
                product_category,
                product_sub_category,
                description,
                unit_price,
                currency,
                sku_code,
                stock_qty,
                uom,
                image_url,
                product_status
            FROM product
            WHERE tenantid = :tenantid
              AND product_id = :product_id
              AND is_deleted = FALSE
              AND status = 'ACTIVE'
        """)

        row = db.execute(
            query,
            {
                "tenantid": tenantid,
                "product_id": product_id,
            },
        ).fetchone()

        if not row:
            return None

        return dict(row._mapping)

    finally:
        db.close()

def update_product(
    tenantid: str,
    product_id: str,
    payload,
    updated_by: str,
):
    db = SessionLocal()

    try:
        query = text("""
            UPDATE product
            SET
                product_name = :product_name,
                product_type = :product_type,
                product_category = :product_category,
                product_sub_category = :product_sub_category,
                description = :description,
                unit_price = :unit_price,
                currency = :currency,
                sku_code = :sku_code,
                stock_qty = :stock_qty,
                uom = :uom,
                image_url = :image_url,
                is_subscription_product = :is_subscription_product,
                tax_code = :tax_code,
                updated_by = :updated_by,
                updated_date = NOW()
            WHERE tenantid = :tenantid
              AND product_id = :product_id
              AND is_deleted = FALSE
        """)

        db.execute(
            query,
            {
                "tenantid": tenantid,
                "product_id": product_id,
                "product_name": payload.product_name,
                "product_type": payload.product_type,
                "product_category": payload.product_category,
                "product_sub_category": payload.product_sub_category,
                "description": payload.description,
                "unit_price": payload.unit_price,
                "currency": payload.currency,
                "sku_code": payload.sku_code,
                "stock_qty": payload.stock_qty,
                "uom": payload.uom,
                "image_url": payload.image_url,
                "is_subscription_product": payload.is_subscription_product,
                "tax_code": payload.tax_code,
                "updated_by": updated_by,
            },
        )

        db.commit()

        return get_product_by_id(
            tenantid,
            product_id,
        )

    finally:
        db.close()


def delete_product(
    tenantid: str,
    product_id: str,
    deleted_by: str,
):
    db = SessionLocal()

    try:
        query = text("""
            UPDATE product
            SET
                is_deleted = TRUE,
                status = 'INACTIVE',
                updated_by = :deleted_by,
                updated_date = NOW()
            WHERE tenantid = :tenantid
              AND product_id = :product_id
        """)

        db.execute(
            query,
            {
                "tenantid": tenantid,
                "product_id": product_id,
                "deleted_by": deleted_by,
            },
        )

        db.commit()

        return {
            "message": "Product deleted successfully"
        }

    finally:
        db.close()                