"""merck_0521_haptic

Revision ID: ff8fcda90104
Revises: a2cce0cf035d
Create Date: 2021-05-20 11:58:12.797568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff8fcda90104'
down_revision = 'a2cce0cf035d'
branch_labels = None
depends_on = None


def upgrade():
    settings_json = """{ "handsFree": false,
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
        """.format(settings_json, warehouse)
        op.execute(sql)


def downgrade():
    pass
