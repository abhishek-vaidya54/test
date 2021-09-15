"""walmartcamerged

Revision ID: ad928c35b90d
Revises: 5a6ca826c31f
Create Date: 2021-07-16 10:53:44.781275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad928c35b90d'
down_revision = '5a6ca826c31f'
branch_labels = None
depends_on = None


def upgrade():
     op.execute(
        """
            UPDATE industrial_athlete SET group_id = 208 WHERE group_id != 208 and warehouse_id = 230;
        """  
    )


def downgrade():
    pass