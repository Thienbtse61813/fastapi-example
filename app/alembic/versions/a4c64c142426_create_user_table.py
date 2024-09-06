"""Create user table

Revision ID: a4c64c142426
Revises: e5051f85d774
Create Date: 2024-09-05 17:56:03.528079

"""
from typing import Sequence, Union
from datetime import datetime
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from app.entities.user import get_password_hash
from app.settings import ADMIN_DEFAULT_PASSWORD


# revision identifiers, used by Alembic.
revision: str = 'a4c64c142426'
down_revision: Union[str, None] = 'e5051f85d774'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_table = op.create_table(
        'users',
        sa.Column('id', sa.UUID, primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=255), nullable=False),
        sa.Column('last_name', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('is_admin', sa.Boolean, nullable=False, default=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    op.create_index("idx_usr_fst_lst_name", "users", ["first_name", "last_name"])
    op.add_column('users', sa.Column('company_id', sa.UUID, nullable=True))
    op.create_foreign_key('fk_usr_cmp', 'users', 'companies', ['company_id'], ['id'])

    op.bulk_insert(user_table, [
        {
            'id': uuid4(),
            'email': 'admin@assignment.com',
            'username': 'admin',
            'first_name': 'Admin',
            'last_name': 'Admin',
            'hashed_password': get_password_hash(ADMIN_DEFAULT_PASSWORD),
            'is_active': True,
            'is_admin': True,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
        }
    ])


def downgrade() -> None:
    op.drop_index("idx_usr_fst_lst_name", table_name='users')
    op.drop_constraint('fk_usr_cmp', 'users', type_='foreignkey')
    op.drop_column('users', 'company_id')
    op.drop_table('users')
