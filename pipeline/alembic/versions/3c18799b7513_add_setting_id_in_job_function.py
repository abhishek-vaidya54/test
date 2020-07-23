"""add_setting_id_in_job_function

Revision ID: 3c18799b7513
Revises: 075c699d6eda
Create Date: 2020-07-23 12:15:51.470604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3c18799b7513"
down_revision = "075c699d6eda"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "job_function",
        sa.Column("settings_id", sa.Integer(), sa.ForeignKey("settings.id")),
    )


def downgrade():
    op.drop_column("settings", "settings_id")
