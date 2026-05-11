from typing import Optional
from pydantic import BaseModel, EmailStr


class RegisterUserDTO(BaseModel):
    first_name: str
    last_name: str
    display_name: str
    email: EmailStr
    phone: Optional[str] = None
    employee_code: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    role_code: str
    password: str


class RegisterUserResponseDTO(BaseModel):
    message: str
    userid: str