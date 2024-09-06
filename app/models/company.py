from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.entities.base_entity import CompanyMode, Rating

class CompanyModel(BaseModel):
    name: str = Field(..., min_length=3, unique=True, max_length=255)
    description: str = Field(..., min_length=3, max_length=255)
    mode: CompanyMode = Field(default=CompanyMode.ACTIVE)
    rating: Rating = Field(default=Rating.NOT_RATED)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Company Name",
                "description": "Company Description",
                "mode": CompanyMode.ACTIVE,
                "rating": Rating.NOT_RATED
            }
        }

class CompanyResponseModel(BaseModel):
    id: UUID
    name: str
    description: str
    mode: CompanyMode = Field(default=CompanyMode.ACTIVE)
    rating: Rating = Field(default=Rating.NOT_RATED)

    class Config:
        from_attributes = True

class CompanySearchModel():
    def __init__(self, name: Optional[str] = None,
                 description: Optional[str] = None,
                 mode: Optional[CompanyMode] = None,
                 rating: Optional[Rating] = None,
                 order_by: Optional[str] = None,
                 order_direction: Optional[str] = None,
                 page: Optional[int] = None,
                 page_size: Optional[int] = None):
        self.name = name
        self.description = description
        self.mode = mode
        self.rating = rating
        self.order_by = order_by
        self.order_direction = order_direction
        self.page = page
        self.page_size = page_size

    class Config:
        from_attributes = True
