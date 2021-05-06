"""wm_canada_groups_override

Revision ID: 0f578005ca5c
Revises: ff505328a1a3
Create Date: 2021-05-06 13:24:37.343471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f578005ca5c'
down_revision = 'ff505328a1a3'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            UPDATE groups SET override_settings=1 WHERE id in [207,208,209];
        """  
    )


def downgrade():
    pass
