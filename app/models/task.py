from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.entities.base_entity import TaskStatus, TaskPriority

class TaskModel(BaseModel):
    summary: str
    description: str
    status: TaskStatus = Field(default=TaskStatus.NOT_STARTED)
    priority: TaskPriority = Field(default=TaskPriority.LOW)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    user_id: UUID

    class Config:
        json_schema_extra = {
            "example": {
                "summary": "Task Summary",
                "description": "Task Description",
                "user_id": "User ID",
                "status": TaskStatus.NOT_STARTED,
                "priority": TaskPriority.LOW
            }
        }

class TaskSearchModel():
    def __init__(self,
                summary: Optional[str] = None,
                description: Optional[str] = None,
                status: Optional[TaskStatus] = None,
                priority: Optional[TaskPriority] = None,
                user_id: Optional[UUID] = None,
                order_by: Optional[str] = None,
                order_direction: Optional[str] = None,
                page: Optional[int] = None,
                page_size: Optional[int] = None):
        self.summary = summary
        self.description = description
        self.status = status
        self.priority = priority
        self.user_id = user_id
        self.order_by = order_by
        self.order_direction = order_direction
        self.page = page
        self.page_size = page_size

    class Config:
        from_attributes = True
