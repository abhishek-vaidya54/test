"""add user warehouse association table

Revision ID: 61bb059d421a
Revises: 02dea1080340
Create Date: 2020-12-07 15:47:15.103262

"""
import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "61bb059d421a"
down_revision = "c9e1ef236af0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_warehouse_association",
        sa.Column(
            "external_admin_user_id", sa.Integer(), nullable=False, primary_key=True
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
            ["warehouse_id"], ["warehouse.id"], name="fk_user_warehouse_assoc_warehouse"
        ),
        sa.ForeignKeyConstraint(
            ["external_admin_user_id"],
            ["external_admin_user.id"],
            name="fk_user_warehouse_assoc_external_admin_user",
        ),
    )


def downgrade():
    op.drop_table("user_warehouse_association")
