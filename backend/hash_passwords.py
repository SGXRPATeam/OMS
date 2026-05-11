from sqlalchemy import text

from app.db.session import SessionLocal
from app.core.security import hash_password

db = SessionLocal()

users = db.execute(
    text("""
        SELECT userid, password_hash
        FROM app_user
    """)
).fetchall()

for user in users:
    current_password = user.password_hash

    # Skip if already hashed
    if current_password.startswith("$2b$"):
        continue

    hashed = hash_password(current_password)

    db.execute(
        text("""
            UPDATE app_user
            SET password_hash = :hashed
            WHERE userid = :userid
        """),
        {
            "hashed": hashed,
            "userid": user.userid,
        },
    )

db.commit()
db.close()

print("Passwords hashed successfully")