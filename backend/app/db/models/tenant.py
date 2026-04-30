from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)

    domains = relationship("TenantDomain", back_populates="tenant")
    users = relationship("User", back_populates="tenant")