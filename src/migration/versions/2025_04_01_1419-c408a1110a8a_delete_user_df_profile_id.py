"""delete_user_df_profile_id

Revision ID: c408a1110a8a
Revises: 0bb1304ef6e2
Create Date: 2025-04-01 14:19:52.560793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'c408a1110a8a'
down_revision: Union[str, None] = '0bb1304ef6e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_profile_id_fkey', 'user', type_='foreignkey')
    op.drop_column('user', 'profile_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profile_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('user_profile_id_fkey', 'user', 'profile', ['profile_id'], ['id'])
    # ### end Alembic commands ###
