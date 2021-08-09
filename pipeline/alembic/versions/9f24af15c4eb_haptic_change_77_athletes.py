"""haptic-change-77-athletes

Revision ID: 9f24af15c4eb
Revises: 88a4b39e5f37
Create Date: 2021-08-09 13:29:55.025568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f24af15c4eb'
down_revision = '88a4b39e5f37'
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
    for industrial_athlete in [1709, 1710, 1711]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}', 'industrial_athlete', {1})
        """.format(jkt_json, industrial_athlete)
        op.execute(sql)

def downgrade():
    pass
