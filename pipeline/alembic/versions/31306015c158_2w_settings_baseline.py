"""2w_settings_baseline

Revision ID: 31306015c158
Revises: 1d9cc1d61fed
Create Date: 2021-06-18 11:32:14.214323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31306015c158'
down_revision = '1d9cc1d61fed'
branch_labels = None
depends_on = None


def upgrade():
    flex_settings = """{ "handsFree": true,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": true,
                "athleteEnabled": true,
                "showEngagement": false,
                "enableProximity": false,
                "showHapticModal": false,
                "enagementEnabled": true,
                "hapticBendNumber": 200,
                "enableTemperature": false,
                "exposureRSSILimit": -48,
                "hapticFeedbackGap": 0,
                "showBaselineModal": true,
                "showSafetyJudgement": false,
                "hapticBendPercentile": 50,
                "hapticFeedbackWindow": 10,
                "showSafetyScoreModal": false,
                "exposureHapticEnabled": false,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 50,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [271, 272, 273, 252]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(flex_settings, warehouse)
        op.execute(sql)

    merck_settings  = """{ "handsFree": false,
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
                "exposureHapticEnabled": true,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 60,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [251]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(merck_settings, warehouse)
        op.execute(sql)
def downgrade():
    pass
