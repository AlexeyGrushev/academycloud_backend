"""Updated user table. Phone removed. Email verify field added

Revision ID: 6242e3cf86a9
Revises: 55fb9694dd6d
Create Date: 2024-03-20 19:29:50.596740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6242e3cf86a9'
down_revision: Union[str, None] = '55fb9694dd6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'classroom', ['id'])
    op.create_unique_constraint(None, 'country', ['id'])
    op.create_unique_constraint(None, 'part_of_speech', ['id'])
    op.create_unique_constraint(None, 'part_of_speech_words', ['id'])
    op.add_column('user', sa.Column('is_verified', sa.Boolean(), nullable=False))
    op.drop_constraint('user_phone_key', 'user', type_='unique')
    op.create_unique_constraint(None, 'user', ['id'])
    op.drop_column('user', 'phone')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('phone', sa.BIGINT(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='unique')
    op.create_unique_constraint('user_phone_key', 'user', ['phone'])
    op.drop_column('user', 'is_verified')
    op.drop_constraint(None, 'part_of_speech_words', type_='unique')
    op.drop_constraint(None, 'part_of_speech', type_='unique')
    op.drop_constraint(None, 'country', type_='unique')
    op.drop_constraint(None, 'classroom', type_='unique')
    # ### end Alembic commands ###
