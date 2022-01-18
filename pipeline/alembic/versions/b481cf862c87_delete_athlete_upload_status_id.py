"""delete athlete_upload_status_id

Revision ID: b481cf862c87
Revises: 68982e963b88
Create Date: 2020-08-21 18:09:06.629114

"""
from alembic import op
from sqlalchemy.engine.reflection import Inspector
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b481cf862c87"
down_revision = "68982e963b88"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()

    if "imported_industrial_athlete" in tables:
        op.drop_table("imported_industrial_athlete")


def downgrade():
    pass
