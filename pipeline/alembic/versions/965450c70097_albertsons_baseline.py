"""albertsons_baseline

Revision ID: 965450c70097
Revises: bad83636f725
Create Date: 2021-07-01 16:26:28.692031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '965450c70097'
down_revision = 'bad83636f725'
branch_labels = None
depends_on = None


def upgrade():
    baseline_settings  = """{ "handsFree": false,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": false,
                "athleteEnabled": false,
                "showEngagement": true,
                "enableProximity": false,
                "showHapticModal": false,
                "enagementEnabled": true,
                "hapticBendNumber": 10,
                "enableTemperature": true,
                "exposureRSSILimit": -48,
                "hapticFeedbackGap": 0,
                "showBaselineModal": true,
                "showSafetyJudgement": true,
                "hapticBendPercentile": 50,
                "hapticFeedbackWindow": 0,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": false,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 60,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [275, 276, 277]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(baseline_settings, warehouse)
        op.execute(sql)


def downgrade():
    pass
