"""alter foreign key constraints email token

Revision ID: 8be9b364cbda
Revises: 1f0755d8788b
Create Date: 2022-09-23 14:44:12.340684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8be9b364cbda"
down_revision = "1f0755d8788b"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint(
        "fk_report_subscribe_email_scheduling_token",
        "email_scheduling_token",
        "foreignkey",
    )
    op.create_foreign_key(
        "fk_report_subscribe_email_scheduling_token",
        "email_scheduling_token",
        "report_subscribe",
        ["report_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint(
        "fk_report_subscribe_email_scheduling_token",
        "email_scheduling_token",
        "foreignkey",
    )
