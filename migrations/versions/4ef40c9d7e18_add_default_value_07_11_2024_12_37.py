"""Add default value 07.11.2024 12:37

Revision ID: 4ef40c9d7e18
Revises: 52d3710ddefd
Create Date: 2024-11-07 12:37:46.964523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ef40c9d7e18'
down_revision: Union[str, None] = '52d3710ddefd'
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
