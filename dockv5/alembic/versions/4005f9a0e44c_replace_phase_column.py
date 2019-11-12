"""replace_phase_column

Revision ID: 4005f9a0e44c
Revises: eb8099f52707
Create Date: 2019-10-18 10:17:06.233296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4005f9a0e44c'
down_revision = 'eb8099f52707'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('dock_phase','phase')
    op.add_column('dock_phase',sa.Column("phase",sa.Enum("DEPLOYED","NOT DEPLOYED","MAINTENANCE"),server_default="NOT DEPLOYED",nullable=False))


def downgrade():
    op.drop_column('dock_phase','phase')
    op.add_column('dock_phase',sa.Column("phase",sa.Enum("PREP","INFIELD","DEMO","MAINTENANCE","UNUSED","RETIRED"),server_default="PREP"))
    
