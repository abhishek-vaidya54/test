"""Create_table_report_subscribe

Revision ID: b48b02b5fcef
Revises: b96c6f2aabdb
Create Date: 2022-04-22 14:30:39.938160

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = 'b48b02b5fcef'
down_revision = 'b96c6f2aabdb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "report_subscribe",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("to_emails", sa.UnicodeText(), nullable=False),
        sa.Column("report_name", sa.Unicode(255), nullable=False),
        sa.Column(
            "subscription_type",
            sa.Enum("Daily", "Weekly", "Monthly"),
            nullable=False,
            default="Daily",
        ),
        sa.Column(
            "subscribed_by",
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
    op.drop_table("report_subscribe")
