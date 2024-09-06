from fastapi import HTTPException, status


class ResourceNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")


class UnAuthorizedError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")

class InvalidTokenError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

class AccessDeniedError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

class InvalidInputError(HTTPException):
    def __init__(self, msg=None):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid input data" if msg is None else msg)

class BusinessRuleViolationError(HTTPException):
    def __init__(self, msg=None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
