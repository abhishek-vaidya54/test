"""remove setting_id imported_industrial_athlete

Revision ID: e7e839bceb04
Revises: 55379c2e7cdc
Create Date: 2020-08-11 19:34:59.532125

"""
from alembic import op
from sqlalchemy.engine.reflection import Inspector
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e7e839bceb04"
down_revision = "55379c2e7cdc"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("imported_industrial_athlete", "setting_id")
    op.drop_column("imported_industrial_athlete", "gender")


def downgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()

    if 'imported_industrial_athlete' in tables:
        op.add_column(
            "imported_industrial_athlete",
            sa.Column("setting_id", sa.Integer(), nullable=False),
        )
        op.add_column(
            "imported_industrial_athlete",
            sa.Column("gender", sa.String(length=1), nullable=True),
        )