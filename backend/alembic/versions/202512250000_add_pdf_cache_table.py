"""add pdf_cache table for hybrid caching

Revision ID: 202512250000
Revises: 202510111000
Create Date: 2025-12-25 00:00:00.000000

This migration creates the pdf_cache table to store preprocessed PDF page data
(word bounding boxes and metadata) in the database for persistence across backend
restarts and horizontal scaling. Images remain in memory cache for performance.

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '202512250000'
down_revision = '202510111000'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create pdf_cache table
    op.create_table(
        'pdf_cache',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('report_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('reports.id', ondelete='CASCADE'), nullable=False),
        sa.Column('page_number', sa.Integer(), nullable=False),
        sa.Column('page_width', sa.Float(), nullable=False),
        sa.Column('page_height', sa.Float(), nullable=False),
        sa.Column('words', postgresql.JSONB(), nullable=False),
        sa.Column('scale', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.UniqueConstraint('report_id', 'page_number', 'scale', name='uq_pdf_cache_report_page_scale'),
    )

    # Create index for faster lookups
    op.create_index(
        'idx_pdf_cache_report_page',
        'pdf_cache',
        ['report_id', 'page_number'],
    )


def downgrade() -> None:
    # Drop index first
    op.drop_index('idx_pdf_cache_report_page', table_name='pdf_cache')

    # Drop table
    op.drop_table('pdf_cache')
