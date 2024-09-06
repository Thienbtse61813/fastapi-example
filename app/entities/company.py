from sqlalchemy import Column, String, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from app.entities.base_entity import BaseEntity, Rating, CompanyMode
from app.database import Base

class Company(BaseEntity, Base):
    __tablename__ = "companies"

    name= Column(String(255), unique=True, nullable=False)
    description= Column(String(255), nullable=True)
    mode= Column(Enum(CompanyMode), nullable=False, default=CompanyMode.ACTIVE)
    rating= Column(Enum(Rating), nullable=False, default=Rating.NOT_RATED)
    users = relationship("User", back_populates="company")
    table_args = (
        UniqueConstraint('name', name='uq_company_name'),
    )

    @classmethod
    def get_sortable_fields(cls):
        return frozenset(cls.__table__.columns.keys()) - {'id'}
