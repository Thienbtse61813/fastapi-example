"""Create task table

Revision ID: a0c66e49684c
Revises: a4c64c142426
Create Date: 2024-09-05 17:56:10.959283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.entities.base_entity import TaskStatus, TaskPriority


# revision identifiers, used by Alembic.
revision: str = 'a0c66e49684c'
down_revision: Union[str, None] = 'a4c64c142426'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID, primary_key=True, nullable=False),
        sa.Column('summary', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('status', sa.Enum(TaskStatus), nullable=False, default=TaskStatus.NOT_STARTED),
        sa.Column('priority', sa.Enum(TaskPriority), nullable=False, default=TaskPriority.LOW),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    op.add_column('tasks', sa.Column('user_id', sa.UUID, nullable=True))
    op.create_foreign_key('fk_tsk_usr', 'tasks', 'users', ['user_id'], ['id'])

def downgrade() -> None:
    op.drop_constraint('fk_tsk_usr', 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'user_id')
    op.drop_table('tasks')
