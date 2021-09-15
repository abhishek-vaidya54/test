"""dart_json_update

Revision ID: 55196d0a0f19
Revises: 6cc5224d7039
Create Date: 2021-06-24 10:27:46.631232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55196d0a0f19'
down_revision = '6cc5224d7039'
branch_labels = None
depends_on = None


def upgrade():
    warehouse_settings  = """{ "handsFree": false,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": false,
                "athleteEnabled": false,
                "showEngagement": true,
                "enableProximity": false,
                "showHapticModal": false,
                "enagementEnabled": true,
                "hapticBendNumber": 8,
                "enableTemperature": true,
                "exposureRSSILimit": -48,
                "hapticFeedbackGap": 0,
                "showBaselineModal": true,
                "showSafetyJudgement": true,
                "hapticBendPercentile": 50,
                "hapticFeedbackWindow": 600000,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": false,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 60,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [259, 260, 261]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(warehouse_settings, warehouse)
        op.execute(sql)


def downgrade():
    pass
