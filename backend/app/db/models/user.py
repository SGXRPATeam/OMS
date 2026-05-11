from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)

    full_name = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))

    tenant = relationship("Tenant", back_populates="users")
    role = relationship("Role", back_populates="users")