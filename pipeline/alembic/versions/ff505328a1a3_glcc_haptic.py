"""glcc_haptic

Revision ID: ff505328a1a3
Revises: 153896d3e27d
Create Date: 2021-05-05 09:46:57.215658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff505328a1a3'
down_revision = '153896d3e27d'
branch_labels = None
depends_on = None


def upgrade():
    settings_json = """{"handsFree": false, "eulaVersion": null, "enableMotion": true, "hapticEnabled": true, "athleteEnabled": false,"showEngagement": true, "enableProximity": false, "showHapticModal": true, "enagementEnabled": true, "hapticBendNumber": 5, "enableTemperature": true, "exposureRSSILimit": -48, "hapticFeedbackGap": 0, "showBaselineModal": false, "showSafetyJudgement": true, "hapticBendPercentile": 50, "hapticFeedbackWindow": 499800, "showSafetyScoreModal": true, "exposureHapticEnabled": true, "exposureHapticRepeatMS": 10000, "hapticSingleBendWindow": 600, "hapticSagAngleThreshold": 75, "exposureHapticSuppressMS": 30000}""".replace('\n', '') 

    for warehouse in [241]:
        sql = """insert into settings (value, target_type, target_id) values ('{0}', 'warehouse', {1})""".format(settings_json, warehouse)
        op.execute(sql)
    
    settings_json = """{"handsFree": false, "eulaVersion": null, "enableMotion": true, "hapticEnabled": true, "athleteEnabled": false,"showEngagement": true, "enableProximity": false, "showHapticModal": true, "enagementEnabled": true, "hapticBendNumber": 5, "enableTemperature": true, "exposureRSSILimit": -48, "hapticFeedbackGap": 0, "showBaselineModal": false, "showSafetyJudgement": true, "hapticBendPercentile": 50, "hapticFeedbackWindow": 600000, "showSafetyScoreModal": true, "exposureHapticEnabled": true, "exposureHapticRepeatMS": 10000, "hapticSingleBendWindow": 600, "hapticSagAngleThreshold": 75, "exposureHapticSuppressMS": 30000}""".replace('\n', '') 

    for warehouse in [242]:
        sql = """insert into settings (value, target_type, target_id) values ('{0}', 'warehouse', {1})""".format(settings_json, warehouse)
        op.execute(sql)

    settings_json = """{"handsFree": false, "eulaVersion": null, "enableMotion": true, "hapticEnabled": false, "athleteEnabled": false,"showEngagement": true, "enableProximity": false, "showHapticModal": true, "enagementEnabled": true, "hapticBendNumber": 1, "enableTemperature": true, "exposureRSSILimit": -48, "hapticFeedbackGap": 0, "showBaselineModal": false, "showSafetyJudgement": true, "hapticBendPercentile": 50, "hapticFeedbackWindow": 0, "showSafetyScoreModal": true, "exposureHapticEnabled": true, "exposureHapticRepeatMS": 10000, "hapticSingleBendWindow": 600, "hapticSagAngleThreshold": 70, "exposureHapticSuppressMS": 30000}""".replace('\n', '') 

    for warehouse in [82, 98, 99, 100, 101, 102, 103, 104, 156, 162, 166, 167, 176, 177, 178, 183, 184, 185, 186, 187]:
        sql = """insert into settings (value, target_type, target_id) values ('{0}', 'warehouse', {1})""".format(settings_json, warehouse)
        op.execute(sql)
    
    settings_json = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": false,
        "enableProximity": false,
        "showHapticModal": false,
        "enagementEnabled": true,
        "hapticBendNumber": 2,
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
        "hapticSagAngleThreshold": 65,
        "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    print(settings_json)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 207);""".format(settings_json)

    print(sql)
    op.execute(sql)

    settings_json = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": false,
        "enableProximity": false,
        "showHapticModal": false,
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
        "exposureHapticEnabled": false,
        "exposureHapticRepeatMS": 10000,
        "hapticSingleBendWindow": 600,
        "hapticSagAngleThreshold": 65,
        "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    print(settings_json)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 208);""".format(settings_json)

    print(sql)
    op.execute(sql)

    settings_json = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": false,
        "enableProximity": false,
        "showHapticModal": false,
        "enagementEnabled": true,
        "hapticBendNumber": 3,
        "enableTemperature": true,
        "exposureRSSILimit": -48,
        "hapticFeedbackGap": 0,
        "showBaselineModal": false,
        "showSafetyJudgement": true,
        "hapticBendPercentile": 50,
        "hapticFeedbackWindow": 480000,
        "showSafetyScoreModal": true,
        "exposureHapticEnabled": false,
        "exposureHapticRepeatMS": 10000,
        "hapticSingleBendWindow": 600,
        "hapticSagAngleThreshold": 65,
        "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    print(settings_json)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 209);""".format(settings_json)

    print(sql)
    op.execute(sql)

    op.execute(
        """
            UPDATE industrial_athlete SET group_id=[207, 208, 209]  WHERE job_function_id in (1513);
        """  
    )


def downgrade():
    pass
