"""remove warehouse_id and role from external_admin_user

Revision ID: 0dfec63dee9c
Revises: 7362f276939c
Create Date: 2021-01-20 13:31:11.632142

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm

# revision identifiers, used by Alembic.
revision = "0dfec63dee9c"
down_revision = "7362f276939c"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    warehouse_id_index = session.execute(
        """
            SHOW INDEXES FROM external_admin_user
            WHERE key_name='fk_ext_admin_user_warehouse'
        """
    ).fetchone()
    session.close()

    if warehouse_id_index:
        op.drop_constraint(
            "fk_ext_admin_user_warehouse", "external_admin_user", "foreignkey"
        )

    op.drop_column("external_admin_user", "warehouse_id")
    op.drop_column("external_admin_user", "role")


def downgrade():
    pass
    # op.add_column(
    #     "external_admin_user",
    #     sa.Column("warehouse_id", sa.Integer(), nullable=False, server_default="45"),
    # )
    # op.add_column(
    #     "external_admin_user",
    #     sa.Column("role", sa.String(length=20), nullable=False),
    # )
    # op.create_foreign_key(
    #     "fk_ext_admin_user_warehouse",
    #     "external_admin_user",
    #     "warehouse",
    #     ["warehouse_id"],
    #     ["id"],
    # )
