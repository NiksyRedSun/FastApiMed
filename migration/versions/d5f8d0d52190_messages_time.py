"""'messages_time'

Revision ID: d5f8d0d52190
Revises: be3baf22eeb7
Create Date: 2024-04-05 21:40:41.588785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5f8d0d52190'
down_revision: Union[str, None] = 'be3baf22eeb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('created_datetime', sa.DateTime(), nullable=True))
    op.drop_column('message', 'created_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('created_date', sa.DATETIME(), nullable=True))
    op.drop_column('message', 'created_datetime')
    # ### end Alembic commands ###