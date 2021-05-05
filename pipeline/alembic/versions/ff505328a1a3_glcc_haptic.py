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


def downgrade():
    pass
