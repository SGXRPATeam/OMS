from app.core.security import verify_password

plain = "admin@123"
hashed = "$2b$12$A6ToAGHrVJKWu1f04.QFfO6S76EXN9p9Cnz1..ixf8sKSKgGcFUxG"

print(verify_password(plain, hashed))