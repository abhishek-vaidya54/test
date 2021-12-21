"""Add_serial_number_in_config_model

Revision ID: 99db6fa2deae
Revises: af7c34ee8bed
Create Date: 2021-12-21 13:29:19.773224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99db6fa2deae'
down_revision = 'af7c34ee8bed'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "config",
        sa.Column(
            "serial_number", sa.String(length=255), nullable=True
        ),
    )


def downgrade():
    op.drop_column("config", "serial_number")
