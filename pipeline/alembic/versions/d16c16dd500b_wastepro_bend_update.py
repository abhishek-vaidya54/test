"""wastepro_bend_update

Revision ID: d16c16dd500b
Revises: ec2d61078e37
Create Date: 2021-06-14 16:21:46.338202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d16c16dd500b"
down_revision = "ec2d61078e37"
branch_labels = None
depends_on = None


def upgrade():
    waste_pro_settings = """{ "handsFree": false,
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
                "hapticFeedbackWindow": 120000,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": true,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 70,
                "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [243, 244, 246, 247, 248, 249]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(
            waste_pro_settings, warehouse
        )
        op.execute(sql)


def downgrade():
    pass
