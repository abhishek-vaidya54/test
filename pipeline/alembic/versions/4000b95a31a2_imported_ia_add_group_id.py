"""imported_ia add group_id

Revision ID: 4000b95a31a2
Revises: 66296d19d35b
Create Date: 2020-08-10 19:07:26.929935

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '4000b95a31a2'
down_revision = '66296d19d35b'
branch_labels = None
depends_on = None


def upgrade():
    sa.Column("group_id", sa.Integer(), nullable=True),


def downgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    
    if 'imported_industrial_athlete' in tables:
        op.drop_column("imported_industrial_athlete", "group_id")
