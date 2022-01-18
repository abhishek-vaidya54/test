"""USCS_newhaptic

Revision ID: 1627b43874bc
Revises: 9eb6e8b682a1
Create Date: 2021-04-23 14:35:52.868779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1627b43874bc"
down_revision = "2af95c711733"
branch_labels = None
depends_on = None


def upgrade():

    settings_json = """{ "handsFree": false,
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
                "exposureHapticEnabled": true,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 70,
                "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [
        136,
        137,
        138,
        139,
        140,
        141,
        189,
        190,
        191,
        192,
        193,
        194,
        195,
        196,
    ]:
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
