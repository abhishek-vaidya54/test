"""2w_handsfree_off

Revision ID: bc2e67312626
Revises: c9ba941eb2a4
Create Date: 2021-08-24 15:48:46.911104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc2e67312626'
down_revision = 'c9ba941eb2a4'
branch_labels = None
depends_on = None


def upgrade():
    ww_settings = """{ "handsFree": false,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": true,
                "athleteEnabled": true,
                "showEngagement": true,
                "enableProximity": false,
                "showHapticModal": false,
                "enagementEnabled": true,
                "hapticBendNumber": 200,
                "enableTemperature": false,
                "exposureRSSILimit": -48,
                "hapticFeedbackGap": 0,
                "showBaselineModal": false,
                "showSafetyJudgement": true,
                "hapticBendPercentile": 50,
                "hapticFeedbackWindow": 10,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": false,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 50,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [271, 272, 273]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(ww_settings, warehouse)
        op.execute(sql)


def downgrade():
    pass