"""remove moderation fields from comments

Revision ID: b248d777cbad
Revises: 392c8cc99e93
Create Date: 2025-10-25 13:36:53.875077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b248d777cbad'
down_revision: Union[str, Sequence[str], None] = '392c8cc99e93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove moderation fields from comments table
    op.drop_column('comments', 'status')
    op.drop_column('comments', 'moderated_at')


def downgrade() -> None:
    """Downgrade schema."""
    # Add back moderation fields to comments table
    op.add_column('comments', sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'))
    op.add_column('comments', sa.Column('moderated_at', sa.DateTime(), nullable=True))
