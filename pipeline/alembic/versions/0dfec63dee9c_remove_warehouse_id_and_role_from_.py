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
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # Need to fix all incorrect dates in table first before running
    session.execute(
        """
            UPDATE external_admin_user SET db_modified_at=CURRENT_TIMESTAMP(), db_created_at=CURRENT_TIMESTAMP()
            WHERE db_created_at='0000-00-00 00:00:00' OR db_modified_at='0000-00-00 00:00:00';
        """
    )
    session.commit()

    op.add_column(
        "external_admin_user",
        sa.Column("warehouse_id", sa.Integer(), nullable=False, server_default="45"),
    )
    op.add_column(
        "external_admin_user",
        sa.Column(
            "role", sa.String(length=20), nullable=False, server_default="manager"
        ),
    )
    op.create_foreign_key(
        "fk_ext_admin_user_warehouse",
        "external_admin_user",
        "warehouse",
        ["warehouse_id"],
        ["id"],
    )

    users = session.execute(
        """
            SELECT u.id, uwa.warehouse_id, ura.role FROM external_admin_user u
            INNER JOIN user_warehouse_association uwa ON (u.id = uwa.external_admin_user_id)
            INNER JOIN user_role_association ura ON (u.id = ura.external_admin_user_id)
        """
    )

    for user in users:
        session.execute(
            f"UPDATE external_admin_user SET warehouse_id={user.warehouse_id}, role='{user.role}' WHERE id={user.id}"
        )

    session.commit()
    session.close()
