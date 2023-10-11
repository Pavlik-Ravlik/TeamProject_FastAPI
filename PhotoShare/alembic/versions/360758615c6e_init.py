"""Init

Revision ID: 360758615c6e
Revises: fcfe92d26dc7
Create Date: 2023-10-11 18:00:40.491036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '360758615c6e'
down_revision: Union[str, None] = 'fcfe92d26dc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=25),
               type_=sa.String(length=255),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=25),
               existing_nullable=False)
    # ### end Alembic commands ###