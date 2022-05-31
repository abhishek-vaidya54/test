"""report_subscribe_warehouse_association

Revision ID: 86bde3c0d58d
Revises: e7804e084064
Create Date: 2022-05-30 14:54:44.890509

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = "86bde3c0d58d"
down_revision = "e7804e084064"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "report_subscribe_warehouse_association",
        sa.Column(
            "report_subscribe_id", sa.Integer(), nullable=False, primary_key=True
        ),
        sa.Column("warehouse_id", sa.Integer(), nullable=False, primary_key=True),
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
            nullable=False,
        ),
        # sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["report_subscribe_id"],
            ["report_subscribe.id"],
            name="fk_association_table_report_subscribe",
        ),
        sa.ForeignKeyConstraint(
            ["warehouse_id"],
            ["warehouse.id"],
            name="fk_association_table_warehouse",
        ),
    )


def downgrade():
    op.drop_table("report_subscribe_warehouse_association")
