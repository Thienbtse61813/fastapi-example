
from datetime import timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.services import user as UserService
from app.database import get_db_context

from app.services.exception import UnAuthorizedError
from app.settings import JWT_ACCESS_TOKEN_EXPIRE_MINUTES

router = None

router = APIRouter(prefix="/auth", tags=["Auth"])
@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db_context)
        ):
            user = UserService.authenticate_user(form_data.username, form_data.password, db)

            if not user:
                raise UnAuthorizedError()

            return {
                "token_type": "bearer",
                "access_token":  UserService.create_access_token(
                    user,
                    int(timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds())
            ),
        }
