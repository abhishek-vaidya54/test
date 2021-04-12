"""roanoke_fixing_warehouse_setting

Revision ID: e5fe9e68ea14
Revises: 624f2cb83417
Create Date: 2021-04-12 14:34:18.661861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5fe9e68ea14'
down_revision = '247eb16e1856'
branch_labels = None
depends_on = None


def upgrade():     

  op.execute( """             
  insert into settings (value, target_type, target_id) values ('{"handsFree":false,"eulaVersion":null,"enableMotion":true,"hapticEnabled":true,"athleteEnabled":true,"showEngagement":true,"enableProximity":false,"showHapticModal":true,"enagementEnabled":true,"hapticBendNumber":3,"enableTemperature":true,"exposureRSSILimit":-48,"hapticFeedbackGap":0,"showBaselineModal":false,"showSafetyJudgement":true,"hapticBendPercentile":50,"hapticFeedbackWindow":300000,"showSafetyScoreModal":true,"exposureHapticEnabled":false,"exposureHapticRepeatMS":10000,"hapticSingleBendWindow":600,"hapticSagAngleThreshold":70,"exposureHapticSuppressMS":30000}', 'warehouse', 220)

"""     )

  op.execute( """             
  insert into settings (value, target_type, target_id) values ('{"handsFree": false, "eulaVersion": null, "enableMotion": true, "hapticEnabled": true, "athleteEnabled": true, "showEngagement": true, "enableProximity": false, "showHapticModal": true, "enagementEnabled": true, "hapticBendNumber": 3, "enableTemperature": true, "exposureRSSILimit": -48, "hapticFeedbackGap": 0, "showBaselineModal": false, "showSafetyJudgement": true, "hapticBendPercentile": 50, "hapticFeedbackWindow": 300000, "showSafetyScoreModal": true, "exposureHapticEnabled": false, "exposureHapticRepeatMS": 10000, "hapticSingleBendWindow": 600, "hapticSagAngleThreshold": 70, "exposureHapticSuppressMS": 30000}', 'group', 204)

"""     )


def downgrade():
    pass
