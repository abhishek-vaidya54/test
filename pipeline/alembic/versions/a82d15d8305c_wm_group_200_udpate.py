"""wm_group_200_udpate

Revision ID: a82d15d8305c
Revises: 1627b43874bc
Create Date: 2021-04-29 09:12:46.605726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a82d15d8305c'
down_revision = '1627b43874bc'
branch_labels = None
depends_on = None


def upgrade():
    settings_json = """{"handsFree": false, "eulaVersion”: null, "enableMotion”: true, "hapticEnabled”: true,
     "athleteEnabled": true, "showEngagement": false, "enableProximity": false, 
     "showHapticModal": false, "enagementEnabled": true, "hapticBendNumber": 
     5, "enableTemperature": true, "exposureRSSILimit": -48, "hapticFeedbackGap": 0,
      "showBaselineModal": false, "showSafetyJudgement": true, "hapticBendPercentile": 50, 
      "hapticFeedbackWindow": 600000, "showSafetyScoreModal": true, "exposureHapticEnabled": false,
       "exposureHapticRepeatMS": 10000, "hapticSingleBendWindow": 600, "hapticSagAngleThreshold": 55,
        "exposureHapticSuppressMS": 30000}""".replace('\n', '')
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 200);""".format(settings_json)
    op.execute(sql)

    op.execute(
        """
            UPDATE groups SET override_settings=1 WHERE id=200;
        """  
    )


def downgrade():
    pass
