"""Alter username column size

Revision ID: d4d537145ac7
Revises: d02757a43ac1
Create Date: 2021-03-17 16:28:02.046646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4d537145ac7'
down_revision = 'd02757a43ac1'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('external_admin_user', 'username',
        existing_type=sa.String(length=36),
        type_=sa.String(length=255),
        existing_nullable=False)    


def downgrade():
    op.alter_column('external_admin_user', 'username',
        existing_type=sa.String(length=255),
        type_=sa.String(length=36),
        existing_nullable=False)    
