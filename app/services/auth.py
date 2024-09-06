from enum import Enum
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

from app.models.user import UserClaims
from app.services.exception import UnAuthorizedError
from app.settings import JWT_SECRET, JWT_ALGORITHM


class LocalAuthorizer:
    security_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

    def __init__(self) -> None:
        pass

    def __call__(self, token: Annotated[str, Depends(security_scheme)] = None):
        if not token:
            raise UnAuthorizedError()

        try:
            claims = jwt.decode(
                token,
                key=JWT_SECRET,
                algorithms=[JWT_ALGORITHM],
                options={
                    "verify_aud": False,
                    "verify_iss": False,
                    "verify_exp": True,
                }
            )
            return UserClaims(**claims)

        except jwt.PyJWTError as err:
            print(err)
            raise UnAuthorizedError()

class CognitoTokenType(Enum):
    ID_TOKEN = "id_token"
    ACCESS_TOKEN = "access_token"
authorizer = LocalAuthorizer()
