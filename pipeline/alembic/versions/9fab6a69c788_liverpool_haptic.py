"""liverpool_haptic

Revision ID: 9fab6a69c788
Revises: 826a1788bc80
Create Date: 2021-07-28 13:18:37.776846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9fab6a69c788"
down_revision = "826a1788bc80"
branch_labels = None
depends_on = None


def upgrade():
    liverpool_settings = """{ "handsFree": false,
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
                "hapticFeedbackWindow": 300000,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": true,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 70,
                "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [258]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(
            liverpool_settings, warehouse
        )
        op.execute(sql)


def downgrade():
    pass
