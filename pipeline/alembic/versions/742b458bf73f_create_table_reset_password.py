"""Create_table_reset_password

Revision ID: 742b458bf73f
Revises: 58a5f8f0b8d8
Create Date: 2022-06-29 17:34:31.446332

"""
from alembic import op
import sqlalchemy as sa
import datetime, uuid


# revision identifiers, used by Alembic.
revision = "742b458bf73f"
down_revision = "58a5f8f0b8d8"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "reset_password",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("external_admin_user.id"),
            nullable=False,
        ),
        sa.Column("ott", sa.UnicodeText(), nullable=False, default=str(uuid.uuid4)),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.Column(
            "db_modified_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            onupdate=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("reset_password")
