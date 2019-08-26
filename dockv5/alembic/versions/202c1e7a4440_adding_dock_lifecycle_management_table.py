"""adding dock lifecycle management table

Revision ID: 202c1e7a4440
Revises: 12c19ccf619c
Create Date: 2019-08-26 10:59:43.920463

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = '202c1e7a4440'
down_revision = '12c19ccf619c'
branch_labels = None
depends_on = None


def upgrade():
    # Generating Dock Lifecycle Management Phase Table
    op.create_table("dock_phase",
    sa.Column("id",sa.Integer(),nullable=False),
    sa.Column("dock_id",sa.String(45),nullable=False),
    sa.Column("timestamp",sa.DateTime,default=datetime.datetime.utcnow,nullable=False),
    sa.Column("phase",sa.Enum("PREP","INFIELD","DEMO","MAINTENANCE","UNUSED","RETIRED"),nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['dock_id'],['config.dock_id'], )
    )


def downgrade():
    # Drops the Dock Lifecycle Management Phase Table
    op.drop_table("dock_phase")
