from typing import Optional
from fastapi import APIRouter, Depends, Query
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_context, get_async_db_context
from app.services.auth import authorizer
from app.services.task import validate_task_params
from app.services import task as TaskService
from app.services.exception import AccessDeniedError
from app.models.user import UserClaims
from app.models.task import TaskModel, TaskSearchModel




router = APIRouter(prefix="/task", tags=["Task"])

@router.get("/")
async def get_all_tasks(db: Session = Depends(get_db_context), user: UserClaims = Depends(authorizer)):
    if not user.is_admin:
        raise AccessDeniedError()
    return TaskService.get_all_tasks(db)

@router.post("/")
async def create_task(request: TaskModel, db: Session = Depends(get_db_context), user: UserClaims = Depends(authorizer)):
    return TaskService.create_task(request, db, user)

@router.get("/search")
@validate_task_params
async def search_tasks(summary: Optional[str] = Query(default=None),
                       description: Optional[str] = Query(default=None),
                       status: Optional[str] = Query(default=None, description="Task status (0: NOT_STARTED, 1: IN_PROGRESS, 2: COMPLETED)"),
                       priority: Optional[str] = Query(default=None, description="Task priority (0: LOW, 1: MEDIUM, 2: HIGH)"),
                       user_id: Optional[UUID] = Query(default=None),
                       order_by: Optional[str] = Query(default=None),
                       order_direction: Optional[str] = Query(default=None),
                       page: Optional[int] = Query(default=None),
                       page_size: Optional[int] = Query(default=None),
                       db: AsyncSession = Depends(get_async_db_context), user: UserClaims = Depends(authorizer)):
    request =  TaskSearchModel(summary, description, status, priority, user_id, order_by, order_direction, page, page_size)
    return await TaskService.search_tasks(request, db, user)

@router.get("/{task_id}")
async def get_task(task_id: UUID, db: Session = Depends(get_db_context), user: UserClaims = Depends(authorizer)):
    return TaskService.get_task(task_id, db, user)

@router.put("/{task_id}")
async def update_task(task_id: UUID, request: TaskModel, db: Session = Depends(get_db_context), user: UserClaims = Depends(authorizer)):
    return TaskService.update_task(task_id, request, db, user)
