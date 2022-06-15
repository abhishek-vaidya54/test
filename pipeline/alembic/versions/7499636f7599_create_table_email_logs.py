"""Create table email logs

Revision ID: 7499636f7599
Revises: b48b02b5fcef
Create Date: 2022-06-14 18:32:05.497171

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = "7499636f7599"
down_revision = "b48b02b5fcef"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "email_logs",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("source_email", sa.String(150), nullable=False),
        sa.Column("destination_email", sa.VARCHAR(255), nullable=False),
        sa.Column("report_subscribed", sa.VARCHAR(255), nullable=False),
        sa.Column("status", sa.VARCHAR(255), nullable=False),
        sa.Column("error_message", sa.VARCHAR(255), nullable=False),
        sa.Column(
            "created_by",
            sa.Integer(),
            sa.ForeignKey("external_admin_user.id"),
            nullable=False,
        ),
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
    op.drop_table("email_logs")
