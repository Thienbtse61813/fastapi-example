from typing import Any, Callable
from functools import wraps
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.company import CompanyModel, CompanySearchModel
from app.services.utils import get_current_utc_time
from app.entities.company import Company
from app.services.exception import BusinessRuleViolationError, ResourceNotFoundError, InvalidInputError
from app.entities.base_entity import CompanyMode, Rating

def create_company(data: CompanyModel, db: Session) -> Company:
    existing_company = db.scalars(select(Company).filter(Company.name == data.name)).first()
    if existing_company:
        raise BusinessRuleViolationError("Company with this name already exists")
    company = Company(**data.model_dump())
    current_time = get_current_utc_time()
    company.created_at = current_time
    company.updated_at = current_time
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

def get_all_companies(db: Session) -> list[Company]:
    return db.scalars(select(Company)).all()

def get_company(company_id: UUID, db: Session) -> Company:
    existing_company = db.scalars(select(Company).filter(Company.id == company_id)).first()
    if not existing_company:
        raise ResourceNotFoundError()
    return existing_company

def update_company(company_id: UUID, data: CompanyModel, db: Session) -> Company:
    existing_company_with_name = db.scalars(select(Company).filter(Company.name == data.name and Company.id != company_id)).first()
    if existing_company_with_name:
        raise BusinessRuleViolationError("Company with this name already exists")
    existing_company = db.scalars(select(Company).filter(Company.id == company_id)).first()
    if not existing_company:
        raise ResourceNotFoundError()
    data.updated_at = get_current_utc_time()
    update_data_dict = data.model_dump(exclude_unset=True)
    for field, value in update_data_dict.items():
        setattr(existing_company, field, value)
    db.commit()
    db.refresh(existing_company)
    return existing_company

async def search_companies(request: CompanySearchModel, db: AsyncSession) -> list[Company]:
    query = select(Company)

    conditions = [
        Company.name.ilike(f"%{request.name}%") if request.name else None,
        Company.description.ilike(f"%{request.description}%") if request.description else None,
        Company.mode == request.mode if request.mode else None,
        Company.rating == request.rating if request.rating else None,
    ]

    query = query.where(*[cond for cond in conditions if cond is not None])

    if request.order_by:
        if request.order_by and request.order_by in Company.get_sortable_fields():
            order_column = getattr(Company, request.order_by)
            query = query.order_by(order_column.desc() if request.order_direction == 'desc' else order_column)
        else:
            raise InvalidInputError("Invalid sort field")

    if request.page and request.page_size:
        query = query.offset((request.page - 1) * request.page_size).limit(request.page_size)
    result = await db.scalars(query)
    return result.all()

def validate_company_params(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        mode = kwargs.get('mode')
        rating = kwargs.get('rating')

        if mode is not None:
            try:
                if isinstance(mode, str):
                    if mode.isdigit():
                        kwargs['mode'] = CompanyMode(int(mode))
                    else:
                        kwargs['mode'] = CompanyMode[mode.upper()]
                elif isinstance(mode, int):
                    kwargs['mode'] = CompanyMode(mode)
            except (ValueError, KeyError):
                raise InvalidInputError("Invalid CompanyMode value")

        if rating is not None:
            try:
                if isinstance(rating, str):
                    if rating.isdigit():
                        kwargs['rating'] = Rating(int(rating))
                    else:
                        kwargs['rating'] = Rating[rating.upper()]
                elif isinstance(rating, int):
                    kwargs['rating'] = Rating(rating)
            except (ValueError, KeyError):
                raise InvalidInputError("Invalid Rating value")

        return await func(*args, **kwargs)
    return wrapper
