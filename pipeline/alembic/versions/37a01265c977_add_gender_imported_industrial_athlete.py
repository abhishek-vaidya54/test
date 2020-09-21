"""add gender imported_industrial_athlete

Revision ID: 37a01265c977
Revises: e7e839bceb04
Create Date: 2020-08-11 19:42:37.427735

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = "37a01265c977"
down_revision = "e7e839bceb04"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "imported_industrial_athlete",
        sa.Column("gender", sa.String(length=1), nullable=True),
    )


def downgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    
    if 'imported_industrial_athlete' in tables:
        op.drop_column("imported_industrial_athlete", "gender")