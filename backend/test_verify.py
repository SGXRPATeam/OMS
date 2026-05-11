from app.core.security import verify_password

stored_hash = "$2b$12$5w6I4Xv3m2P9m6xW0z6o3u5xQ2mM7VxQ4M9X0QmQjJ2q7cP0a7v8K"

print(
    verify_password(
        "admin123",
        stored_hash,
    )
)