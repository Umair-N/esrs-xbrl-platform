"""add_image_to_pdf_cache

Revision ID: 52c283ceb2ac
Revises: cb8e3776383b
Create Date: 2025-10-25 14:45:20.236566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52c283ceb2ac'
down_revision: Union[str, Sequence[str], None] = 'cb8e3776383b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add image column to pdf_cache table for persistent image caching."""
    op.add_column('pdf_cache', sa.Column('image', sa.LargeBinary(), nullable=True))


def downgrade() -> None:
    """Remove image column from pdf_cache table."""
    op.drop_column('pdf_cache', 'image')
