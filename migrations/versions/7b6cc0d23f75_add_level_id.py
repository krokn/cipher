"""add level_id

Revision ID: 7b6cc0d23f75
Revises: f66a97ea7e1c
Create Date: 2024-07-26 15:28:45.839563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b6cc0d23f75'
down_revision: Union[str, None] = 'f66a97ea7e1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('level_id', sa.Integer(), nullable=False))
    op.drop_constraint('users_level_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(None, 'users', 'levels', ['level_id'], ['id'])
    op.drop_column('users', 'level')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('level', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.create_foreign_key('users_level_fkey', 'users', 'levels', ['level'], ['id'])
    op.drop_column('users', 'level_id')
    # ### end Alembic commands ###
