from typing import List
from pydantic import BaseModel


class TenantInfo(BaseModel):
    tenantid: str
    tenant_name: str
    role_code: str
    role: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    userid: str
    tenantid: str
    role: str
    email: str
    display_name: str
    tenants: List[TenantInfo]


class SwitchTenantRequest(BaseModel):
    tenantid: str


class SwitchTenantResponse(BaseModel):
    access_token: str
    token_type: str
    tenantid: str
    role: str