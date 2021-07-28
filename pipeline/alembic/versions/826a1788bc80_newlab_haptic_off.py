"""newlab_haptic_off

Revision ID: 826a1788bc80
Revises: 3b47de732b03
Create Date: 2021-07-28 10:32:09.593414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '826a1788bc80'
down_revision = '3b47de732b03'
branch_labels = None
depends_on = None


def upgrade():
     json_settings = """{ "handsFree": false,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": false,
                "athleteEnabled": false,
                "showEngagement": true,
                "enableProximity": false,
                "showHapticModal": false,
                "enagementEnabled": true,
                "hapticBendNumber": 3,
                "enableTemperature": true,
                "exposureRSSILimit": -48,
                "hapticFeedbackGap": 0,
                "showBaselineModal": true,
                "showSafetyJudgement": true,
                "hapticBendPercentile": 50,
                "hapticFeedbackWindow": 120000,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": true,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 70,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [77]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(     json_settings = """{ "handsFree": false,
, warehouse)
        op.execute(sql)


def downgrade():
    pass
