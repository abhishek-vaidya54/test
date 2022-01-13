"""metadata table

Revision ID: 2efae14f67f9
Revises: 70dbc5719915
Create Date: 2019-08-22 11:57:39.780046

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = "2efae14f67f9"
down_revision = "70dbc5719915"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "metadata",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.String(length=45), nullable=False),
        sa.Column("processed_file_id", sa.Integer(), nullable=False),
        sa.Column("metadata_type", sa.String(length=255), nullable=False),
        sa.Column("value", sa.String(length=255), nullable=False),
        sa.Column("exclude", sa.Boolean(), default=0, nullable=False),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.Column("notes", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["processed_file_id"], ["processed_file.id"], name="activity_ibfk_3"
        ),
    )


def downgrade():
    op.drop_table("metadata")
