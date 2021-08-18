"""06142021_settings_changes

Revision ID: ec2d61078e37
Revises: 29781eb89dbb
Create Date: 2021-06-14 10:49:17.178086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec2d61078e37'
down_revision = '29781eb89dbb'
branch_labels = None
depends_on = None


def upgrade():
    dallas_settings_json = """{ "handsFree": false,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": true,
                "athleteEnabled": false,
                "showEngagement": true,
                "enableProximity": false,
                "showHapticModal": true,
                "enagementEnabled": true,
                "hapticBendNumber": 4,
                "enableTemperature": true,
                "exposureRSSILimit": -48,
                "hapticFeedbackGap": 0,
                "showBaselineModal": false,
                "showSafetyJudgement": true,
                "hapticBendPercentile": 50,
                "hapticFeedbackWindow": 400200,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": true,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 60,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [265]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(dallas_settings_json, warehouse)
        op.execute(sql)

    houston_settings_json = """{ "handsFree": false,
            "eulaVersion": null,
            "enableMotion": true,
            "hapticEnabled": true,
            "athleteEnabled": false,
            "showEngagement": true,
            "enableProximity": false,
            "showHapticModal": true,
            "enagementEnabled": true,
            "hapticBendNumber": 4,
            "enableTemperature": true,
            "exposureRSSILimit": -48,
            "hapticFeedbackGap": 0,
            "showBaselineModal": false,
            "showSafetyJudgement": true,
            "hapticBendPercentile": 50,
            "hapticFeedbackWindow": 400200,
            "showSafetyScoreModal": true,
            "exposureHapticEnabled": true,
            "exposureHapticRepeatMS": 10000,
            "hapticSingleBendWindow": 600,
            "hapticSagAngleThreshold": 65,
            "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [262]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(houston_settings_json, warehouse)
        op.execute(sql)

    philadelphia_settings_json = """{ "handsFree": false,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": true,
                "athleteEnabled": false,
                "showEngagement": true,
                "enableProximity": false,
                "showHapticModal": true,
                "enagementEnabled": true,
                "hapticBendNumber": 5,
                "enableTemperature": true,
                "exposureRSSILimit": -48,
                "hapticFeedbackGap": 0,
                "showBaselineModal": false,
                "showSafetyJudgement": true,
                "hapticBendPercentile": 50,
                "hapticFeedbackWindow": 499800,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": true,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 60,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [263]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(philadelphia_settings_json, warehouse)
        op.execute(sql)

    sacramento_settings_json = """{ "handsFree": false,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": true,
                "athleteEnabled": false,
                "showEngagement": true,
                "enableProximity": false,
                "showHapticModal": true,
                "enagementEnabled": true,
                "hapticBendNumber": 3,
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
                "hapticSagAngleThreshold": 60,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [264]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(sacramento_settings_json, warehouse)
        op.execute(sql)
    
    waste_pro_settings = """{ "handsFree": false,
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
                "hapticFeedbackWindow": 120000,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": true,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 70,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [243, 244, 246, 247, 248, 249]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(waste_pro_settings, warehouse)
        op.execute(sql)

    albertsons_settings = """{ "handsFree": false,
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
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [220, 221]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(albertsons_settings, warehouse)
        op.execute(sql)
        

    
def downgrade():
    pass
