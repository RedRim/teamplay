"""init

Revision ID: f2a1dc4037f3
Revises: 8c90e06c0678
Create Date: 2025-04-05 13:27:17.406742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f2a1dc4037f3'
down_revision: Union[str, None] = '8c90e06c0678'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('post_author_id_fkey', 'post', type_='foreignkey')
    op.drop_column('post', 'author_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('post_author_id_fkey', 'post', 'uuser', ['author_id'], ['id'])
    # ### end Alembic commands ###
