"""merge_heads

Revision ID: cb8e3776383b
Revises: 202512250000, 5a8ae085d607
Create Date: 2025-10-25 14:45:01.374442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb8e3776383b'
down_revision: Union[str, Sequence[str], None] = ('202512250000', '5a8ae085d607')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
