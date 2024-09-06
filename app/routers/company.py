from fastapi import APIRouter, Depends, Query
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db_context, get_async_db_context
from app.models.company import CompanyModel, CompanyResponseModel, CompanySearchModel
from app.models.user import UserClaims
from app.services import company as CompanyService
from app.services.auth import authorizer
from app.services.company import validate_company_params
from app.services.exception import AccessDeniedError




router = APIRouter(
    prefix="/company",
    tags=["Company"],
)

@router.get("/")
async def get_all_companies(db: Session = Depends(get_db_context), user: UserClaims = Depends(authorizer)):
    if not user.is_admin:
        raise AccessDeniedError()
    return CompanyService.get_all_companies(db)

@router.post("/", response_model=CompanyResponseModel)
async def create_company(request: CompanyModel, db: Session = Depends(get_db_context), user: UserClaims = Depends(authorizer)):
    if not user.is_admin:
        raise AccessDeniedError()
    return CompanyService.create_company(request, db)

@router.get("/search", response_model=list[CompanyResponseModel])
@validate_company_params
async def search_companies(name: Optional[str] = Query(default=None),
                           description: Optional[str] = Query(default=None),
                           mode: Optional[str] = Query(default=None, description="Company mode (0: INACTIVE, 1: ACTIVE)"),
                           rating: Optional[str] = Query(default=None, description="Company rating (0: NOT_RATED, 1: ONE, 2: TWO, 3: THREE, 4: FOUR, 5: FIVE)"),
                           order_by: Optional[str] = Query(default=None),
                           order_direction: Optional[str] = Query(default=None),
                           page: Optional[int] = Query(default=None),
                           page_size: Optional[int] = Query(default=None),
                           db: AsyncSession = Depends(get_async_db_context), user: UserClaims = Depends(authorizer)):
    if not user.is_admin:
        raise AccessDeniedError()
    request = CompanySearchModel(name, description, mode, rating, order_by, order_direction, page, page_size)
    return await CompanyService.search_companies(request, db)

@router.get("/{company_id}", response_model=CompanyResponseModel)
async def get_company(company_id: UUID, db: Session = Depends(get_db_context), user: UserClaims = Depends(authorizer)):
    if not user.is_admin and user.company_id != str(company_id):
        raise AccessDeniedError()
    return CompanyService.get_company(company_id, db)

@router.put("/{company_id}", response_model=CompanyResponseModel)
async def update_company(company_id: UUID, request: CompanyModel, db: Session = Depends(get_db_context), user: UserClaims = Depends(authorizer)):
    if not user.is_admin:
        raise AccessDeniedError()
    return CompanyService.update_company(company_id, request, db)
