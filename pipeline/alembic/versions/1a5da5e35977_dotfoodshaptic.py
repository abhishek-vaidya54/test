"""dotfoodshaptic

Revision ID: 1a5da5e35977
Revises: 729417177e51
Create Date: 2021-08-04 09:21:30.378779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a5da5e35977'
down_revision = '729417177e51'
branch_labels = None
depends_on = None


def upgrade():
    mtsterling_settings = """{ "handsFree": false,
            "eulaVersion": null,
            "enableMotion": true,
            "hapticEnabled": true,
            "athleteEnabled": false,
            "showEngagement": true,
            "enableProximity": false,
            "showHapticModal": true,
            "enagementEnabled": true,
            "hapticBendNumber": 2,
            "enableTemperature": true,
            "exposureRSSILimit": -48,
            "hapticFeedbackGap": 0,
            "showBaselineModal": false,
            "showSafetyJudgement": true,
            "hapticBendPercentile": 50,
            "hapticFeedbackWindow": 300000,
            "showSafetyScoreModal": true,
            "exposureHapticEnabled": true,
            "exposureHapticRepeatMS": 10000,
            "hapticSingleBendWindow": 600,
            "hapticSagAngleThreshold": 70,
            "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [256]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(mtsterling_settings, warehouse)
        op.execute(sql)

    chi_settings = """{ "handsFree": false,
            "eulaVersion": null,
            "enableMotion": true,
            "hapticEnabled": true,
            "athleteEnabled": false,
            "showEngagement": true,
            "enableProximity": false,
            "showHapticModal": true,
            "enagementEnabled": true,
            "hapticBendNumber": 2,
            "enableTemperature": true,
            "exposureRSSILimit": -48,
            "hapticFeedbackGap": 0,
            "showBaselineModal": false,
            "showSafetyJudgement": true,
            "hapticBendPercentile": 50,
            "hapticFeedbackWindow": 300000,
            "showSafetyScoreModal": true,
            "exposureHapticEnabled": true,
            "exposureHapticRepeatMS": 10000,
            "hapticSingleBendWindow": 600,
            "hapticSagAngleThreshold": 70,
            "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [257]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(chi_settings, warehouse)
        op.execute(sql)

def downgrade():
    pass
