from typing import Optional
from datetime import timedelta
from uuid import UUID
import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.settings import JWT_ALGORITHM, JWT_SECRET, JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from app.entities.user import User, verify_password, get_password_hash
from app.services.utils import get_current_utc_time, get_current_timestamp
from app.models.user import UserModel, UserUpdateModel, UserSearchModel, UserClaims
from app.services.exception import BusinessRuleViolationError, ResourceNotFoundError, InvalidInputError
from app.entities.company import Company

def create_access_token(user: User, expires: Optional[int] = None):
    claims = UserClaims(
        sub=str(user.id),
        username=user.username,
        email=user.email,
        is_admin=user.is_admin,
        is_active=user.is_active,
        aud='FastAPI',
        iss='FastAPI',
        iat=get_current_timestamp(),
        exp=get_current_timestamp() + expires if expires else get_current_timestamp() + int(timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds())
    )
    return jwt.encode(claims.model_dump(), JWT_SECRET, algorithm=JWT_ALGORITHM)

def authenticate_user(username: str, password: str, db: Session):
    user = db.scalars(select(User).filter(User.username == username)).first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_all_users(db: Session):
    return db.scalars(select(User)).all()

def create_user(request: UserModel, db: Session) -> User:
    existing_user = db.scalars(select(User).filter(User.email == request.email or User.username == request.username)).first()
    if existing_user:
        raise BusinessRuleViolationError("User with this email or username already exists")
    existing_company = db.scalars(select(Company).filter(Company.id == request.company_id)).first()
    if not existing_company:
        raise ResourceNotFoundError("Company not found")
    current_time = get_current_utc_time()
    user = User(
        username=request.username,
        email=request.email,
        first_name=request.first_name,
        last_name=request.last_name,
        company_id=request.company_id,
        created_at=current_time,
        updated_at=current_time,
        hashed_password=get_password_hash(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(user_id: UUID, request: UserUpdateModel, db: Session, logged_in_user: UserClaims) -> User:
    user_with_update_email = db.scalars(select(User).filter(User.email == request.email and User.id != user_id)).first()
    if user_with_update_email:
        raise BusinessRuleViolationError("User with this email already exists")
    existing_user = db.scalars(select(User).filter(User.id == user_id)).first()
    if not existing_user:
        raise ResourceNotFoundError("User not found")
    existing_user.updated_at = get_current_utc_time()
    if logged_in_user.is_admin:
        # Admin can update more fields
        map_user_model_to_user(existing_user, request)
    else:
        # Not Admin can not update is_admin, is_active, company_id
        print(request.is_admin, request.is_active, request.company_id)
        if request.is_admin or request.is_active or request.company_id:
            raise BusinessRuleViolationError("You are not allowed to update this field")
        else:
            map_user_model_to_user(existing_user, request)

    db.commit()
    db.refresh(existing_user)
    return existing_user

def search_users(request: UserSearchModel, db: Session) -> list[User]:
    query = select(User)

    conditions = [
        User.email.ilike(f"%{request.email}%") if request.email else None,
        User.username.ilike(f"%{request.username}%") if request.username else None,
        User.first_name.ilike(f"%{request.first_name}%") if request.first_name else None,
        User.last_name.ilike(f"%{request.last_name}%") if request.last_name else None,
        User.company_id == request.company_id if request.company_id else None,
        User.is_admin == request.is_admin if request.is_admin else None,
        User.is_active == request.is_active if request.is_active else None,
    ]

    query = query.where(*[cond for cond in conditions if cond is not None])

    if request.order_by:
        if request.order_by and request.order_by in User.get_sortable_fields():
            order_column = getattr(User, request.order_by)
            query = query.order_by(order_column.desc() if request.order_direction == 'desc' else order_column)
        else:
            raise InvalidInputError("Invalid sort field")

    if request.page and request.page_size:
        query = query.offset((request.page - 1) * request.page_size).limit(request.page_size)
    return db.scalars(query).all()

def get_user(user_id: UUID, db: Session) -> User:
    user = db.scalars(select(User).filter(User.id == user_id)).first()
    if not user:
        raise ResourceNotFoundError("User not found")
    return user

def map_user_model_to_user(user: User, request: UserModel) -> User:
    update_data_dict = request.model_dump(exclude_unset=True)
    for field, value in update_data_dict.items():
        if field == 'password':
            setattr(user, 'hashed_password', get_password_hash(value))
        else:
            setattr(user, field, value)
    return user
