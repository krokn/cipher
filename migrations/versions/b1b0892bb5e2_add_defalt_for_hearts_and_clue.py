"""add defalt for hearts and clue

Revision ID: b1b0892bb5e2
Revises: 7654d5e5ca0b
Create Date: 2024-07-07 20:42:29.877348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1b0892bb5e2'
down_revision: Union[str, None] = '7654d5e5ca0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###