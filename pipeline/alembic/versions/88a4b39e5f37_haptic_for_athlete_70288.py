"""haptic_for_athlete_70288

Revision ID: 88a4b39e5f37
Revises: 729417177e51
Create Date: 2021-08-03 14:52:46.868699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88a4b39e5f37'
down_revision = '729417177e51'
branch_labels = None
depends_on = None


def upgrade():
    jkt_json = """{ "handsFree": false,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": true,
                "athleteEnabled": false,
                "showEngagement": true,
                "enableProximity": false,
                "showHapticModal": true,
                "enagementEnabled": true,
                "hapticBendNumber": 1,
                "enableTemperature": true,
                "exposureRSSILimit": -48,
                "hapticFeedbackGap": 0,
                "showBaselineModal": false,
                "showSafetyJudgement": true,
                "hapticBendPercentile": 50,
                "hapticFeedbackWindow": 0,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": false,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 60,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    sql = """  
        insert into settings (value, target_type, target_id) values ('{0}', 'industrial_athlete', {1}) """.format(jkt_json, 70288)
    op.execute(sql)


def downgrade():
    pass
