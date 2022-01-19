"""add_roles_table

Revision ID: 5ccb06675357
Revises: a0ee75053872
Create Date: 2020-07-30 15:15:25.874741

"""
import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5ccb06675357"
down_revision = "a0ee75053872"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=36), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
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
        # sa.ForeignKeyConstraint(
        #     ["username"], ["external_admin_user.id"], name="fk_ex_admin_user_role"
        # ),
    )


def downgrade():
    op.drop_table("roles")
