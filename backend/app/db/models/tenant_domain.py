from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class TenantDomain(Base):
    __tablename__ = "tenant_domains"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, nullable=False, unique=True)

    tenant_id = Column(Integer, ForeignKey("tenants.id"))

    tenant = relationship("Tenant", back_populates="domains")