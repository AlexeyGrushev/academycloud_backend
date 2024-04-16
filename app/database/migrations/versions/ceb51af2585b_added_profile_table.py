"""Added profile table

Revision ID: ceb51af2585b
Revises: 6242e3cf86a9
Create Date: 2024-04-09 08:41:36.965030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ceb51af2585b'
down_revision: Union[str, None] = '6242e3cf86a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_data', sa.BigInteger(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('profile_picture', sa.String(), nullable=True),
    sa.Column('status', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['user_data'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.drop_table('country')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('country',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('country', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='country_pkey'),
    sa.UniqueConstraint('country', name='country_country_key'),
    sa.UniqueConstraint('id', name='country_id_key')
    )
    op.drop_table('profile')
    # ### end Alembic commands ###
