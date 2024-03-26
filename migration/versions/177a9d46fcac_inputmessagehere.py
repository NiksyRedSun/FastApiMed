"""'INPUTMESSAGEHERE'

Revision ID: 177a9d46fcac
Revises: 
Create Date: 2024-03-11 22:13:17.479380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '177a9d46fcac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('archer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('attack', sa.Integer(), nullable=True),
    sa.Column('defense', sa.Integer(), nullable=True),
    sa.Column('agility', sa.Integer(), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=True),
    sa.Column('max_hp', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bar',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('cur_level', sa.Integer(), nullable=True),
    sa.Column('money_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('skins_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('wood_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('time_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('time_for_archer', sa.Integer(), nullable=True),
    sa.Column('archers', sa.Integer(), nullable=True),
    sa.Column('max_archers', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('citizen',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('attack', sa.Integer(), nullable=True),
    sa.Column('defense', sa.Integer(), nullable=True),
    sa.Column('agility', sa.Integer(), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=True),
    sa.Column('max_hp', sa.Integer(), nullable=True),
    sa.Column('duty', sa.Enum('just_citizen', 'peasant', 'woodcutter', 'huntsman', 'militia', name='myenum'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fields',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('cur_level', sa.Integer(), nullable=True),
    sa.Column('money_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('time_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('time_for_res_pack', sa.Integer(), nullable=True),
    sa.Column('res_per_worker', sa.Float(), nullable=True),
    sa.Column('workers', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hunter_house',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('cur_level', sa.Integer(), nullable=True),
    sa.Column('money_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('time_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('time_for_res_pack', sa.Integer(), nullable=True),
    sa.Column('res_per_worker', sa.Float(), nullable=True),
    sa.Column('workers', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('money', sa.Integer(), nullable=True),
    sa.Column('wood', sa.Integer(), nullable=True),
    sa.Column('wheat', sa.Integer(), nullable=True),
    sa.Column('skins', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('knight',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('attack', sa.Integer(), nullable=True),
    sa.Column('defense', sa.Integer(), nullable=True),
    sa.Column('agility', sa.Integer(), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=True),
    sa.Column('max_hp', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('market',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('cur_level', sa.Integer(), nullable=True),
    sa.Column('money_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('skins_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('wood_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('wheat_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('taxes', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tower',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('cur_level', sa.Integer(), nullable=True),
    sa.Column('money_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('wood_for_next_lvl', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('town_square',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('cur_level', sa.Integer(), nullable=True),
    sa.Column('money_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('wheat_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('wood_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('time_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('time_for_citizen', sa.Integer(), nullable=True),
    sa.Column('time_for_money_pack', sa.Integer(), nullable=True),
    sa.Column('money_per_citizens', sa.Float(), nullable=True),
    sa.Column('citizens_in_city', sa.Integer(), nullable=True),
    sa.Column('unemployed_citizens', sa.Integer(), nullable=True),
    sa.Column('max_citizens', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('war_house',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('cur_level', sa.Integer(), nullable=True),
    sa.Column('money_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('skins_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('wood_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('time_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('time_for_knight', sa.Integer(), nullable=True),
    sa.Column('knights', sa.Integer(), nullable=True),
    sa.Column('max_knights', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wood_house',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('cur_level', sa.Integer(), nullable=True),
    sa.Column('money_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('time_for_next_lvl', sa.Integer(), nullable=True),
    sa.Column('time_for_res_pack', sa.Integer(), nullable=True),
    sa.Column('res_per_worker', sa.Float(), nullable=True),
    sa.Column('workers', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wood_house')
    op.drop_table('war_house')
    op.drop_table('town_square')
    op.drop_table('tower')
    op.drop_table('market')
    op.drop_table('knight')
    op.drop_table('inventory')
    op.drop_table('hunter_house')
    op.drop_table('fields')
    op.drop_table('citizen')
    op.drop_table('bar')
    op.drop_table('archer')
    op.drop_table('user')
    # ### end Alembic commands ###