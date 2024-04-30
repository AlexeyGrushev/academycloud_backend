"""Updated user.role column

Revision ID: 27611acf17ef
Revises: fdc2192c54a2
Create Date: 2024-04-28 00:52:39.583252

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27611acf17ef'
down_revision: Union[str, None] = 'fdc2192c54a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'role',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.create_foreign_key(None, 'user', 'role', ['role'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.alter_column('user', 'role',
               existing_type=sa.BIGINT(),
               nullable=True)
    # ### end Alembic commands ###
