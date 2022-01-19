"""creating_external_admin_user_table

Revision ID: ae41b9b137af
Revises: 1fa42a92b557
Create Date: 2020-03-27 18:39:22.922055

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = "ae41b9b137af"
down_revision = "1fa42a92b557"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "external_admin_user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=36), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
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
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["warehouse_id"], ["warehouse.id"], name="fk_ext_admin_user_warehouse"
        ),
        sa.ForeignKeyConstraint(
            ["client_id"], ["client.id"], name="fk_ext_admin_user_client"
        ),
    )


def downgrade():
    op.drop_table("external_admin_user")
