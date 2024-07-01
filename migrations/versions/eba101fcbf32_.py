"""empty message

Revision ID: eba101fcbf32
Revises: 
Create Date: 2024-06-29 16:33:05.141566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eba101fcbf32'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reputation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code_length', sa.Integer(), nullable=True),
    sa.Column('hint', sa.Integer(), nullable=True),
    sa.Column('degree_hint', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('subscription_status', sa.Integer(), nullable=True),
    sa.Column('hearts', sa.Integer(), nullable=True),
    sa.Column('clue', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('current_level', sa.Integer(), nullable=True),
    sa.Column('reputation', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rating')
    op.drop_table('users')
    op.drop_table('reputation')
    # ### end Alembic commands ###
