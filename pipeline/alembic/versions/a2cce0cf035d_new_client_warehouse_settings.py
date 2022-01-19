"""new_client_warehouse_settings

Revision ID: a2cce0cf035d
Revises: dca6817709bb
Create Date: 2021-05-17 09:45:20.207794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a2cce0cf035d"
down_revision = "dca6817709bb"
branch_labels = None
depends_on = None


def upgrade():
    dot_foods_hd_supply_settings_json = """{ "handsFree": false,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": false,
                "athleteEnabled": false,
                "showEngagement": true,
                "enableProximity": false,
                "showHapticModal": false,
                "enagementEnabled": true,
                "hapticBendNumber": 1,
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
                "hapticSagAngleThreshold": 70,
                "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [262, 263, 264, 265, 258, 257, 256]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(
            dot_foods_hd_supply_settings_json, warehouse
        )
        op.execute(sql)

    # primoris_settings_json = """{ "handsFree": false,
    #             "eulaVersion": null,
    #             "enableMotion": true,
    #             "hapticEnabled": false,
    #             "athleteEnabled": false,
    #             "showEngagement": true,
    #             "enableProximity": true,
    #             "showHapticModal": false,
    #             "enagementEnabled": true,
    #             "hapticBendNumber": 1,
    #             "enableTemperature": true,
    #             "exposureRSSILimit": -48,
    #             "hapticFeedbackGap": 0,
    #             "showBaselineModal": true,
    #             "showSafetyJudgement": true,
    #             "hapticBendPercentile": 50,
    #             "hapticFeedbackWindow": 0,
    #             "showSafetyScoreModal": true,
    #             "exposureHapticEnabled": false,
    #             "exposureHapticRepeatMS": 10000,
    #             "hapticSingleBendWindow": 600,
    #             "hapticSagAngleThreshold": 70,
    #             "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    # for warehouse in [270]:
    #     sql = """
    #         insert into settings (value, target_type, target_id)
    #         values ('{0}',
    #             'warehouse', {1})
    #     """.format(primoris_settings_json, warehouse)
    #     op.execute(sql)


def downgrade():
    pass
