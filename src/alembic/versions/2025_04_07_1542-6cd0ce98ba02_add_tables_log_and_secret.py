"""add tables log and secret

Revision ID: 6cd0ce98ba02
Revises: 
Create Date: 2025-04-07 15:42:47.958295

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '6cd0ce98ba02'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('secret_key', sa.Uuid(), nullable=False),
    sa.Column('action', sa.Enum('create', 'get', 'delete', name='action'), nullable=False),
    sa.Column('ip_address', sa.String(), nullable=False),
    sa.Column('ttl_seconds', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('secret',
    sa.Column('secret_key', sa.Uuid(), nullable=False),
    sa.Column('secret', sa.LargeBinary(), nullable=False),
    sa.Column('passphrase', sa.String(), nullable=True),
    sa.Column('ttl_seconds', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('secret_key')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('secret')
    op.drop_table('log')
    sa.Enum('create', 'get', 'delete', name='action').drop(op.get_bind())
