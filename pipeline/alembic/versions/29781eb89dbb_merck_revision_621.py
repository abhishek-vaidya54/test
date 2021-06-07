"""merck_revision_621

Revision ID: 29781eb89dbb
Revises: c4c906a89913
Create Date: 2021-06-01 16:03:57.433172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29781eb89dbb'
down_revision = 'c4c906a89913'
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
                "hapticBendNumber": 2,
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
