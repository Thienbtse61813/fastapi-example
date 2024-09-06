import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, DateTime, UUID


class Rating(Enum):
    NOT_RATED = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

class TaskStatus(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2

class CompanyMode(Enum):
    ACTIVE = 1
    INACTIVE = 0

class TaskPriority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class BaseEntity:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
