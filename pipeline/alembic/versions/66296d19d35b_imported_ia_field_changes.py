"""imported_ia field changes

Revision ID: 66296d19d35b
Revises: 32f25afc98ce
Create Date: 2020-08-10 18:58:25.487536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "66296d19d35b"
down_revision = "32f25afc98ce"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("imported_industrial_athlete", "setting_id")
    op.drop_column("imported_industrial_athlete", "schedule")
    op.drop_column("imported_industrial_athlete", "prior_back_injuries")
    op.drop_column("imported_industrial_athlete", "group_id")


def downgrade():
    pass
