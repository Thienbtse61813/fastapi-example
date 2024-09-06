from uuid import UUID
from typing import Any, Callable
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.task import TaskModel, TaskSearchModel
from app.entities.task import Task
from app.services.utils import get_current_utc_time
from app.entities.base_entity import TaskStatus, TaskPriority
from app.services.exception import BusinessRuleViolationError, ResourceNotFoundError, AccessDeniedError, InvalidInputError
from app.models.user import UserClaims

def get_all_tasks(db: Session):
    return db.query(select(Task)).all()

def create_task(request: TaskModel, db: Session, user: UserClaims):
    if not user.is_admin and user.sub != str(request.user_id):
        raise BusinessRuleViolationError("You are not allowed to create task for this user")
    if request.status == TaskStatus.IN_PROGRESS:
        count_of_in_progress_tasks = db.scalar(
        select(func.count()).where(
            (Task.status == TaskStatus.IN_PROGRESS) and
            (str(Task.user_id) == str(request.user_id))
        )
        )
        if count_of_in_progress_tasks >= 2:
            raise BusinessRuleViolationError("User can have only 2 in progress tasks")
    db_task = Task(**request.model_dump())
    current_time = get_current_utc_time()
    db_task.created_at = current_time
    db_task.updated_at = current_time
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(task_id: UUID, request: TaskModel, db: Session, user: UserClaims):
    existing_task = db.query(Task).filter(Task.id == task_id).first()
    if not existing_task:
        raise ResourceNotFoundError("Task not found")
    if not user.is_admin and user.sub != str(request.user_id):
        raise BusinessRuleViolationError("You are not allowed to update")
    update_data_dict = request.model_dump(exclude_unset=True)
    for field, value in update_data_dict.items():
        setattr(existing_task, field, value)
    existing_task.updated_at = get_current_utc_time()
    db.commit()
    db.refresh(existing_task)
    return existing_task

def get_task(task_id: int, db: Session, user: UserClaims):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise ResourceNotFoundError("Task not found")
    if not user.is_admin and user.sub != str(task.user_id):
        raise AccessDeniedError()
    return task

async def search_tasks(request: TaskSearchModel, db: AsyncSession, user: UserClaims) -> list[Task]:
    if request.user_id and not user.is_admin and user.sub != str(request.user_id):
        raise BusinessRuleViolationError("You are not allowed to search tasks for this user")
    query = select(Task)
    conditions = [
        Task.summary.ilike(f"%{request.summary}%") if request.summary else None,
        Task.description.ilike(f"%{request.description}%") if request.description else None,
        Task.status == request.status if request.status else None,
        Task.priority == request.priority if request.priority else None,
        Task.user_id == request.user_id if request.user_id else None,
    ]
    query = query.where(*[cond for cond in conditions if cond is not None])

    if request.order_by:
        if request.order_by and request.order_by in Task.get_sortable_fields():
            order_column = getattr(Task, request.order_by)
            query = query.order_by(order_column.desc() if request.order_direction == 'desc' else order_column)
        else:
            raise InvalidInputError("Invalid sort field")

    if request.page and request.page_size:
        query = query.offset((request.page - 1) * request.page_size).limit(request.page_size)
    result = await db.scalars(query)
    return result.all()


def validate_task_params(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        status = kwargs.get('status')
        priority = kwargs.get('priority')

        if status is not None:
            try:
                if isinstance(status, str):
                    if status.isdigit():
                        kwargs['status'] = TaskStatus(int(status))
                    else:
                        kwargs['status'] = TaskStatus[status.upper()]
                elif isinstance(status, int):
                    kwargs['status'] = TaskStatus(status)
            except (ValueError, KeyError):
                raise InvalidInputError("Invalid TaskStatus value")

        if priority is not None:
            try:
                if isinstance(priority, str):
                    if priority.isdigit():
                        kwargs['priority'] = TaskPriority(int(priority))
                    else:
                        kwargs['priority'] = TaskPriority[priority.upper()]
                elif isinstance(priority, int):
                    kwargs['priority'] = TaskPriority(priority)
            except (ValueError, KeyError):
                raise InvalidInputError("Invalid TaskPriority value")

        return await func(*args, **kwargs)
    return wrapper
