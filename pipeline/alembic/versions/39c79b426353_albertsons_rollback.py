"""albertsons_rollback

Revision ID: 39c79b426353
Revises: d16c16dd500b
Create Date: 2021-06-14 16:38:12.847404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39c79b426353'
down_revision = 'd16c16dd500b'
branch_labels = None
depends_on = None


def upgrade():
    roanoake_settings = """{ "handsFree": false,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": true,
                "athleteEnabled": true,
                "showEngagement": true,
                "enableProximity": false,
                "showHapticModal": true,
                "enagementEnabled": true,
                "hapticBendNumber": 3,
                "enableTemperature": true,
                "exposureRSSILimit": -48,
                "hapticFeedbackGap": 0,
                "showBaselineModal": false,
                "showSafetyJudgement": true,
                "hapticBendPercentile": 50,
                "hapticFeedbackWindow": 300000,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": false,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 70,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [220]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(roanoake_settings, warehouse)
        op.execute(sql)

    lancaster_settings = """{ "handsFree": false,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": true,
                "athleteEnabled": true,
                "showEngagement": true,
                "enableProximity": false,
                "showHapticModal": true,
                "enagementEnabled": true,
                "hapticBendNumber": 4,
                "enableTemperature": true,
                "exposureRSSILimit": -48,
                "hapticFeedbackGap": 0,
                "showBaselineModal": false,
                "showSafetyJudgement": true,
                "hapticBendPercentile": 50,
                "hapticFeedbackWindow": 600000,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": false,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 70,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [221]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(lancaster_settings, warehouse)
        op.execute(sql)


def downgrade():
    pass
