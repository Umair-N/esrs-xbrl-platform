"""create editor sessions table

Revision ID: 222222222222
Revises: f28769ef4842
Create Date: 2025-09-09 00:00:00.000000

This migration introduces a new table for persisting user‑specific
editor sessions. Each session stores the full JSON document and
metadata such as a human‑friendly name and timestamps. Sessions are
associated with users via a foreign key. The table uses a UUID as its
primary key to avoid collisions across distributed systems and
separates session storage from the existing reports infrastructure.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '222222222222'
down_revision: Union[str, Sequence[str], None] = 'f28769ef4842'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema by creating the editor_sessions table."""
    op.create_table(
        'editor_sessions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('data', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema by dropping the editor_sessions table."""
    op.drop_table('editor_sessions')