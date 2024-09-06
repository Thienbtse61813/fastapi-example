"""Create company table

Revision ID: e5051f85d774
Revises:
Create Date: 2024-09-05 17:55:34.439589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.entities.base_entity import Rating, CompanyMode



# revision identifiers, used by Alembic.
revision: str = 'e5051f85d774'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'companies',
        sa.Column('id', sa.UUID, primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('mode', sa.Enum(CompanyMode), nullable=False, default=CompanyMode.ACTIVE),
        sa.Column('rating', sa.Enum(Rating), nullable=False, default=Rating.NOT_RATED),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('companies')
    op.execute('DROP TYPE rating')
