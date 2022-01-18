"""summerville_rssi_update

Revision ID: dca6817709bb
Revises: b42664120d3d
Create Date: 2021-05-11 16:03:31.389888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dca6817709bb"
down_revision = "b42664120d3d"
branch_labels = None
depends_on = None


def upgrade():
    settings_json = """{"handsFree": true,"eulaVersion": null,"enableMotion": false,"hapticEnabled": false,"athleteEnabled": true,"showEngagement": false,"enableProximity": true,"showHapticModal": false,"enagementEnabled": false,"hapticBendNumber": 0,"enableTemperature": false,"exposureRSSILimit": -58,"hapticFeedbackGap": 0,"showBaselineModal": false,"showSafetyJudgement": true,"hapticBendPercentile": 0,"hapticFeedbackWindow": 0,"showSafetyScoreModal": false,"exposureHapticEnabled": true,"exposureHapticRepeatMS": 10000,"hapticSingleBendWindow": 0,"hapticSagAngleThreshold": 0,"exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [172]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(
            settings_json, warehouse
        )
        op.execute(sql)


def downgrade():
    pass
