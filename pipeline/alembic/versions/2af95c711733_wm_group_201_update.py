"""WM group 201 update

Revision ID: 2af95c711733
Revises: 9eb6e8b682a1
Create Date: 2021-04-27 18:01:39.449359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2af95c711733"
down_revision = "9eb6e8b682a1"
branch_labels = None
depends_on = None


def upgrade():
    settings_json = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": false,
        "enableProximity": false,
        "showHapticModal": false,
        "enagementEnabled": true,
        "hapticBendNumber": 4,
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
        "hapticSagAngleThreshold": 75,
        "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    print(settings_json)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 206);""".format(
        settings_json
    )

    print(sql)
    op.execute(sql)

    op.execute(
        """
            UPDATE industrial_athlete SET group_id=206 WHERE job_function_id in (1217, 1218, 1219, 1220, 1243);
        """
    )

    op.execute(
        """
            UPDATE groups SET override_settings=1 WHERE id=206;
        """
    )


def downgrade():
    pass
