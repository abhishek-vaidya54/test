"""2w_update_setting

Revision ID: c9ba941eb2a4
Revises: 98f1c94e9fa3
Create Date: 2021-08-20 11:40:28.504638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c9ba941eb2a4"
down_revision = "98f1c94e9fa3"
branch_labels = None
depends_on = None


def upgrade():
    flex_settings = """{ "handsFree": true,
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
                "showBaselineModal": true,
                "showSafetyJudgement": true,
                "hapticBendPercentile": 50,
                "hapticFeedbackWindow": 10,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": false,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 50,
                "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [271, 272, 273]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(
            flex_settings, warehouse
        )
        op.execute(sql)


def downgrade():
    pass
