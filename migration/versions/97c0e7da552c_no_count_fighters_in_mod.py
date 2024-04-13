"""'no_count_fighters_in_mod'

Revision ID: 97c0e7da552c
Revises: 2c8d587eb0c4
Create Date: 2024-04-13 23:00:05.581767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97c0e7da552c'
down_revision: Union[str, None] = '2c8d587eb0c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bar', 'archers')
    op.drop_column('war_house', 'knights')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('war_house', sa.Column('knights', sa.INTEGER(), nullable=True))
    op.add_column('bar', sa.Column('archers', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###