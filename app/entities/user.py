from passlib.context import CryptContext

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.entities.base_entity import BaseEntity


bcrypt_context = CryptContext(schemes=["bcrypt"])

class User(BaseEntity, Base):
    __tablename__ = "users"

    email= Column(String(255), unique=True, nullable=False)
    username= Column(String(255), unique=True, nullable=False)
    first_name= Column(String(255), nullable=False)
    last_name= Column(String(255), nullable=False)
    hashed_password= Column(String(255), nullable=False)
    is_active= Column(Boolean, default=True)
    is_admin= Column(Boolean, default=False)
    company_id= Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)

    company= relationship("Company", back_populates="users")
    tasks = relationship("Task", back_populates="user")

    @classmethod
    def get_sortable_fields(cls):
        return frozenset(cls.__table__.columns.keys()) - {'id'}

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hased_password):
    return bcrypt_context.verify(plain_password, hased_password)
