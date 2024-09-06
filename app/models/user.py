from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class UserModel(BaseModel):
    username: str = Field(..., unique=True, min_length=3, max_length=255)
    password: str = Field(..., min_length=8, max_length=255)
    first_name: str = Field(..., min_length=3, max_length=255)
    last_name: str = Field(..., min_length=3, max_length=255)
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)
    email: str = Field(..., unique=True, min_length=3, max_length=255)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    company_id: UUID

    class Config:
        json_schema_extra = {
            "example": {
                "username": "Username",
                "password": "password",
                "email": "Email",
                "company_id": "Company ID",
                "first_name": "First Name",
                "last_name": "Last Name",
                "is_admin": False,
                "is_active": True,
            }
        }

class UserResponseModel(BaseModel):
    id: UUID
    username: str
    first_name: str
    last_name: str
    is_admin: bool
    is_active: bool
    email: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    company_id: Optional[UUID] = None

    class Config:
        from_attributes = True

class UserUpdateModel(BaseModel):
    password: Optional[str] = Field(min_length=8, max_length=255)
    first_name: Optional[str] = Field(min_length=3, max_length=255)
    last_name: Optional[str] = Field(min_length=3, max_length=255)
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None
    email: Optional[str] = Field(unique=True, min_length=3, max_length=255)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    company_id: Optional[UUID] = None

    class Config:
        json_schema_extra = {
            "example": {
                "password": "password",
                "email": "Email",
                "company_id": "Company ID",
                "first_name": "First Name",
                "last_name": "Last Name",
                "is_admin": False,
                "is_active": True,
                "company_id": "Company ID",
            }
        }

class UserClaims(BaseModel):
    sub: str
    username: str = None
    email: str = None
    is_admin: bool = None
    is_active: bool = None
    company_id: Optional[UUID] = None
    aud: str = None
    iss: str = None
    iat: int
    exp: int

class UserSearchModel():
    def __init__(self, email: Optional[str] = None,
                 username: Optional[str] = None,
                 first_name: Optional[str] = None,
                 last_name: Optional[str] = None,
                 company_id: Optional[UUID] = None,
                 is_admin: Optional[bool] = None,
                 is_active: Optional[bool] = None,
                 order_by: Optional[str] = None,
                 order_direction: Optional[str] = None,
                 page: Optional[int] = None,
                 page_size: Optional[int] = None):
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.company_id = company_id
        self.is_admin = is_admin
        self.is_active = is_active
        self.order_by = order_by
        self.order_direction = order_direction
        self.page = page
        self.page_size = page_size

    class Config:
        from_attributes = True
