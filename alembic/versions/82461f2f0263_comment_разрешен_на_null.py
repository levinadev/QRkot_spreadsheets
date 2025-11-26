"""comment разрешен на null

Revision ID: 82461f2f0263
Revises: d96484c6fbde
Create Date: 2025-11-17 19:26:35.763751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82461f2f0263'
down_revision = 'd96484c6fbde'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.alter_column(
            'comment',
            existing_type=sa.TEXT(),
            nullable=True
        )


def downgrade():
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.alter_column(
            'comment',
            existing_type=sa.TEXT(),
            nullable=False
        )
