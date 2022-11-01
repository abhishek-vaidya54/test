"""Drop table EmailSchedulingToken

Revision ID: 0b49da425038
Revises: 8be9b364cbda
Create Date: 2022-10-31 13:48:36.782953

"""
from alembic import op
import sqlalchemy as sa
import datetime, uuid


# revision identifiers, used by Alembic.
revision = "0b49da425038"
down_revision = "8be9b364cbda"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint(
        "fk_report_subscribe_email_scheduling_token",
        "email_scheduling_token",
        "foreignkey",
    )
    op.drop_table("email_scheduling_token")


def downgrade():
    op.create_table(
        "email_scheduling_token",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("report_id", sa.Integer(), nullable=False),
        sa.Column("token_id", sa.UnicodeText(), nullable=False, default=uuid.uuid4),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["report_id"],
            ["report_subscribe.id"],
            name="fk_report_subscribe_email_scheduling_token",
        ),
    )
