"""add is_active to industrial_athlete

Revision ID: c77a08526ef7
Revises: 75c576d02328
Create Date: 2020-10-29 12:57:07.377806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c77a08526ef7"
down_revision = "75c576d02328"
branch_labels = None
depends_on = None


def upgrade():
    print("Skipping")
    # try:
    #     op.execute("DROP INDEX `external_id` ON industrial_athlete")
    # except:
    #     pass
    # finally:
    #     op.add_column(
    #         "industrial_athlete",
    #         sa.Column("is_active", sa.Boolean(), nullable=True, server_default=None),
    #     )
    #     op.execute(
    #         """
    #             ALTER TABLE industrial_athlete
    #             ADD CONSTRAINT external_id_warehouse_id_is_active
    #             UNIQUE (external_id, warehouse_id, is_active);
    #         """
    #     )


def downgrade():
    print("Skipping")
    # try:
    #     op.execute(
    #         "ALTER TABLE industrial_athlete ADD UNIQUE (external_id, warehouse_id, termination_date);"
    #     )
    # except:
    #     pass
    # finally:
    #     op.drop_column("industrial_athlete", "is_active")
    #     op.execute(
    #         "DROP INDEX `external_id_warehouse_id_is_active` ON industrial_athlete"
    #     )
