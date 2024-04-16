"""Update profile table

Revision ID: a5d12396140e
Revises: ceb51af2585b
Create Date: 2024-04-12 21:30:43.907842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5d12396140e'
down_revision: Union[str, None] = 'ceb51af2585b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('profile', 'last_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.create_unique_constraint(None, 'profile', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'profile', type_='unique')
    op.alter_column('profile', 'last_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###
