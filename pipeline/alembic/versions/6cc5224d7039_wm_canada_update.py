"""wm_canada_update

Revision ID: 6cc5224d7039
Revises: 15d94d1d8ceb
Create Date: 2021-06-21 22:07:34.088348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cc5224d7039'
down_revision = '15d94d1d8ceb'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            UPDATE groups SET override_settings=1 WHERE id in (207,208,209);
        """  
    )

    settings_json_groupa_canada = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": true,
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

    print(settings_json_groupa_canada)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 207);""".format(settings_json_groupa_canada)

    print(sql)
    op.execute(sql)

    settings_json_groupb_canada = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": true,
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

    print(settings_json_groupb_canada)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 208);""".format(settings_json_groupb_canada)

    print(sql)
    op.execute(sql)

    settings_json_groupc_canada = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": true,
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

    print(settings_json_groupc_canada)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 209);""".format(settings_json_groupc_canada)

    print(sql)
    op.execute(sql)

def downgrade():
    pass
