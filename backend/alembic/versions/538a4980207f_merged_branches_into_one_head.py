"""Merged branches into one head

Revision ID: 538a4980207f
Revises: 222222222222, 93f4ef8703b5
Create Date: 2025-09-18 11:10:25.149829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '538a4980207f'
down_revision: Union[str, Sequence[str], None] = ('222222222222', '93f4ef8703b5')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
