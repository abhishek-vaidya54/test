"""crestmead_haptic

Revision ID: 153896d3e27d
Revises: a82d15d8305c
Create Date: 2021-05-04 16:07:37.615672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '153896d3e27d'
down_revision = 'a82d15d8305c'
branch_labels = None
depends_on = None


def upgrade():
    settings_json = """{"handsFree": false, "eulaVersion": null, "enableMotion": true, "hapticEnabled": true, "athleteEnabled": false,"showEngagement": true, "enableProximity": false, "showHapticModal": true, "enagementEnabled": true, "hapticBendNumber": 2, "enableTemperature": true, "exposureRSSILimit": -48, "hapticFeedbackGap": 0, "showBaselineModal": false, "showSafetyJudgement": true, "hapticBendPercentile": 50, "hapticFeedbackWindow": 0, "showSafetyScoreModal": true, "exposureHapticEnabled": true, "exposureHapticRepeatMS": 10000, "hapticSingleBendWindow": 600, "hapticSagAngleThreshold": 70, "exposureHapticSuppressMS": 30000}""".replace('\n', '') 

    for warehouse in [235]:

        sql = """insert into settings (value, target_type, target_id) values ('{0}', 'warehouse', {1})""".format(settings_json, warehouse)

op.execute(sql)


def downgrade():
    pass
