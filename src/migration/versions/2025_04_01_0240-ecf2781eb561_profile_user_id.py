"""profile_user_id

Revision ID: ecf2781eb561
Revises: 029228201b96
Create Date: 2025-04-01 02:40:23.635156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ecf2781eb561'
down_revision: Union[str, None] = '029228201b96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profile', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'profile', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'profile', type_='foreignkey')
    op.drop_column('profile', 'user_id')
    # ### end Alembic commands ###
