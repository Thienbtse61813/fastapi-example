from app.database import Base
from sqlalchemy import Column, String, Enum, ForeignKey, Uuid
from sqlalchemy.orm import relationship
from app.entities.base_entity import BaseEntity, TaskStatus, TaskPriority


class Task(BaseEntity, Base):
    __tablename__ = "tasks"

    summary= Column(String(255), nullable=False)
    description= Column(String(255), nullable=True)
    status= Column(Enum(TaskStatus), nullable=False, default=TaskStatus.NOT_STARTED)
    priority= Column(Enum(TaskPriority), nullable=False, default=TaskPriority.LOW)
    user_id= Column(Uuid, ForeignKey('users.id'), nullable=True)

    user= relationship("User", back_populates="tasks")


    @classmethod
    def get_sortable_fields(cls):
        return frozenset(cls.__table__.columns.keys()) - {'id'}
