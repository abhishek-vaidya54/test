"""creastmead_groups_052821

Revision ID: c4c906a89913
Revises: c98b2ed86844
Create Date: 2021-05-28 13:32:11.768583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4c906a89913'
down_revision = 'c98b2ed86844'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            UPDATE groups SET override_settings=1 WHERE id=214;
        """  
    )

    warehouse_settings_json = """{ "handsFree": false,
            "eulaVersion": null,
            "enableMotion": true,
            "hapticEnabled": false,
            "athleteEnabled": false,
            "showEngagement": true,
            "enableProximity": false,
            "showHapticModal": false,
            "enagementEnabled": false,
            "hapticBendNumber": 1,
            "enableTemperature": true,
            "exposureRSSILimit": -48,
            "hapticFeedbackGap": 0,
            "showBaselineModal": true,
            "showSafetyJudgement": true,
            "hapticBendPercentile": 50,
            "hapticFeedbackWindow": 0,
            "showSafetyScoreModal": true,
            "exposureHapticEnabled": true,
            "exposureHapticRepeatMS": 10000,
            "hapticSingleBendWindow": 600,
            "hapticSagAngleThreshold": 70,
            "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [235]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(warehouse_settings_json, warehouse)
        op.execute(sql)

    group_settings_json = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": false,
        "showEngagement": false,
        "enableProximity": false,
        "showHapticModal": false,
        "enagementEnabled": true,
        "hapticBendNumber": 4,
        "enableTemperature": true,
        "exposureRSSILimit": -48,
        "hapticFeedbackGap": 120000,
        "showBaselineModal": false,
        "showSafetyJudgement": true,
        "hapticBendPercentile": 50,
        "hapticFeedbackWindow": 300000,
        "showSafetyScoreModal": true,
        "exposureHapticEnabled": false,
        "exposureHapticRepeatMS": 10000,
        "hapticSingleBendWindow": 600,
        "hapticSagAngleThreshold": 70,
        "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    print(group_settings_json)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 214);""".format(group_settings_json)

    print(sql)
    op.execute(sql)

    op.execute(
        """
            UPDATE industrial_athlete SET group_id=214 WHERE id in (71928, 71929, 71932, 71934, 71946, 71952, 71953, 71955, 71927, 71930, 71931, 71933, 71942, 71943, 71945, 71954, 71145, 71146, 71147, 71148, 71149, 71150, 71151, 71184, 71185, 71920, 71956);
        """  
    )

    


def downgrade():
    pass
