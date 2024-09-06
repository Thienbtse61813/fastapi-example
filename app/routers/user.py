from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session

from app.database import get_db_context
from app.services import user as UserService
from app.services.auth import authorizer
from app.services.exception import AccessDeniedError
from app.models.user import UserClaims, UserResponseModel, UserUpdateModel, UserModel, UserSearchModel

router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@router.get("/", response_model=list[UserResponseModel])
async def get_all_users(db: Session = Depends(get_db_context), user: UserClaims = Depends(authorizer)):
    if not user.is_admin:
        raise AccessDeniedError()
    return UserService.get_all_users(db)

@router.post("/", response_model=UserResponseModel)
async def create_user(request: UserModel, db: Session = Depends(get_db_context), user: UserClaims = Depends(authorizer)):
    if not user.is_admin:
        raise AccessDeniedError()
    return UserService.create_user(request, db)

@router.get("/search", response_model=list[UserResponseModel])
async def search_users(
    email: Optional[str] = Query(default=None),
    username: Optional[str] = Query(default=None),
    first_name: Optional[str] = Query(default=None),
    last_name: Optional[str] = Query(default=None),
    company_id: Optional[UUID] = Query(default=None),
    is_admin: Optional[bool] = Query(default=None),
    is_active: Optional[bool] = Query(default=None),
    order_by: Optional[str] = Query(default=None),
    order_direction: Optional[str] = Query(default=None),
    page: Optional[int] = Query(default=None),
    page_size: Optional[int] = Query(default=None),
    db: Session = Depends(get_db_context),
    user: UserClaims = Depends(authorizer)
):
    if not user.is_admin:
        raise AccessDeniedError()
    request = UserSearchModel(email, username, first_name, last_name, company_id, is_admin, is_active, order_by, order_direction, page, page_size)
    return UserService.search_users(request, db)

@router.put("/{user_id}", response_model=UserResponseModel)
async def update_user(user_id: UUID, request: UserUpdateModel, db: Session = Depends(get_db_context), user: UserClaims = Depends(authorizer)):
    if not user.is_admin and user.sub != str(user_id):
        raise AccessDeniedError()
    return UserService.update_user(user_id, request, db, user)

@router.get("/{user_id}", response_model=UserResponseModel)
async def get_user(user_id: UUID, db: Session = Depends(get_db_context), user: UserClaims = Depends(authorizer)):
    if not user.is_admin and user.sub != str(user_id):
        raise AccessDeniedError()
    return UserService.get_user(user_id, db)
