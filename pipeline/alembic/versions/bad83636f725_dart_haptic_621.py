"""dart_haptic_621

Revision ID: bad83636f725
Revises: 55196d0a0f19
Create Date: 2021-06-25 14:15:02.806905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bad83636f725"
down_revision = "55196d0a0f19"
branch_labels = None
depends_on = None


def upgrade():
    mtm_settings = """{ "handsFree": false,
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
                "hapticFeedbackWindow": 21600000,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": false,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 60,
                "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [259]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(
            mtm_settings, warehouse
        )
        op.execute(sql)

    mason_settings = """{ "handsFree": false,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": true,
                "athleteEnabled": false,
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
                "hapticFeedbackWindow": 600000,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": false,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 60,
                "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [260]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(
            mason_settings, warehouse
        )
        op.execute(sql)

    shipping_settings = """{ "handsFree": false,
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
                "exposureHapticEnabled": false,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 60,
                "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [261]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(
            shipping_settings, warehouse
        )
        op.execute(sql)


def downgrade():
    pass
