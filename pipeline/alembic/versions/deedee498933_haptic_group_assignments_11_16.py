"""haptic group assignments 11 16

Revision ID: deedee498933
Revises: 3cbf6936f0aa
Create Date: 2020-11-16 11:53:23.699412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'deedee498933'
down_revision = '3cbf6936f0aa'
branch_labels = None
depends_on = None


def upgrade():
    pass
    # op.execute(
    #     """
    #         update industrial_athlete set group_id = 177 where id in (24333,24336,30822,30823,24305,24318,24317,24303,24307,24315,24306,24302,30214,24296,24291,24293,24290,24288,28219,28210,28215,31335,30393,24368,24353,24357,24351,24339,24343,24356,24347,24360,24344,24350,30215,30209,28217,25491,31727,31341,31346,30394,24411,24420,24395,24400,24413,24409,24399,24398,24416,24410,24397,24401,24412,24414,24406,31330,24378,24390,24379,24381,24383,24388,24386,24385,31888,24374,24373,24375,31626,31629,24342,30217,30211,30213,30218,28212,28213,28214,24394,28216,24319,24337,31333,30389,31340,24403,24355,24312,30820,24325,24332,31331)
    #     """
    # )


def downgrade():
    pass
