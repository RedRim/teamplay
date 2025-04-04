"""profile_user_type_null_true

Revision ID: f2552e935d69
Revises: ecf2781eb561
Create Date: 2025-04-01 02:42:50.924578

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f2552e935d69'
down_revision: Union[str, None] = 'ecf2781eb561'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('profile', 'user_type',
               existing_type=postgresql.ENUM('USER', 'PRO', 'MANAGER', 'ADMIN', name='usertype'),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('profile', 'user_type',
               existing_type=postgresql.ENUM('USER', 'PRO', 'MANAGER', 'ADMIN', name='usertype'),
               nullable=False)
    # ### end Alembic commands ###
