"""dotfoodssterling

Revision ID: 377e5ec93402
Revises: 9f24af15c4eb
Create Date: 2021-08-12 19:17:39.993700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "377e5ec93402"
down_revision = "9f24af15c4eb"
branch_labels = None
depends_on = None


def upgrade():
    mtsterling_settings = """{ "handsFree": false,
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

    for warehouse in [256]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(
            mtsterling_settings, warehouse
        )
        op.execute(sql)


def downgrade():
    pass
