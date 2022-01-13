"""crestmead2

Revision ID: 08d52832ea79
Revises: bc2e67312626
Create Date: 2021-08-25 16:26:01.993546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "08d52832ea79"
down_revision = "bc2e67312626"
branch_labels = None
depends_on = None


def upgrade():
    warehouse_settings_json = """{ "handsFree": false,
            "eulaVersion": null,
            "enableMotion": true,
            "hapticEnabled": false,
            "athleteEnabled": false,
            "showEngagement": true,
            "enableProximity": false,
            "showHapticModal": false,
            "enagementEnabled": false,
            "hapticBendNumber": 4,
            "enableTemperature": true,
            "exposureRSSILimit": -48,
            "hapticFeedbackGap": 120000,
            "showBaselineModal": true,
            "showSafetyJudgement": true,
            "hapticBendPercentile": 50,
            "hapticFeedbackWindow": 300000,
            "showSafetyScoreModal": true,
            "exposureHapticEnabled": true,
            "exposureHapticRepeatMS": 10000,
            "hapticSingleBendWindow": 600,
            "hapticSagAngleThreshold": 70,
            "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [332]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(
            warehouse_settings_json, warehouse
        )
        op.execute(sql)


def downgrade():
    pass
