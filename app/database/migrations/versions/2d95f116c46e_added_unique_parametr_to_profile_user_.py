"""Added unique parametr to profile.user_data table

Revision ID: 2d95f116c46e
Revises: f147ff26daa3
Create Date: 2024-05-18 01:31:03.549315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d95f116c46e'
down_revision: Union[str, None] = 'f147ff26daa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'profile', ['user_data'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'profile', type_='unique')
    # ### end Alembic commands ###
