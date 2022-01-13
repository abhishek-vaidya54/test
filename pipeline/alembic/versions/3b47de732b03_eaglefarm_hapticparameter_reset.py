"""EagleFarm_HapticParameter_Reset

Revision ID: 3b47de732b03
Revises: ad928c35b90d
Create Date: 2021-07-19 21:42:23.513288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3b47de732b03"
down_revision = "ad928c35b90d"
branch_labels = None
depends_on = None


def upgrade():
    metcash_eaglefarm_settings = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": true,
        "enableProximity": false,
        "showHapticModal": true,
        "enagementEnabled": true,
        "hapticBendNumber": 2,
        "enableTemperature": true,
        "exposureRSSILimit": -48,
        "hapticFeedbackGap": 300000,
        "showBaselineModal": false,
        "showSafetyJudgement": true,
        "hapticBendPercentile": 50,
        "hapticFeedbackWindow": 396000,
        "showSafetyScoreModal": true,
        "exposureHapticEnabled": false,
        "exposureHapticRepeatMS": 10000,
        "hapticSingleBendWindow": 600,
        "hapticSagAngleThreshold": 70,
        "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [228]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(
            metcash_eaglefarm_settings, warehouse
        )
        op.execute(sql)


def downgrade():
    pass
