"""create canvas states table

Revision ID: 202510111000
Revises: 93f4ef8703b5
Create Date: 2025-10-11 10:00:00.000000

This migration introduces a new table for persisting saved editor
canvas states. Each canvas state stores the full serialized report
document along with optional metadata such as a human‑friendly name
and timestamps. The table is tied to the ``users`` table via a
foreign key on ``user_id``. Using a UUID primary key ensures that
records can be created concurrently across distributed systems
without collision.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '202510111000'
down_revision: Union[str, Sequence[str], None] = '93f4ef8703b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema by creating the canvas_states table."""
    op.create_table(
        'canvas_states',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('report_id', sa.String(length=255), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('data', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema by dropping the canvas_states table."""
    op.drop_table('canvas_states')