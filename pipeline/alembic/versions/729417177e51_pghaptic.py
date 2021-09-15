"""pghaptic

Revision ID: 729417177e51
Revises: 9fab6a69c788
Create Date: 2021-08-02 08:48:49.249626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '729417177e51'
down_revision = '9fab6a69c788'
branch_labels = None
depends_on = None


def upgrade():
    jkt_json = """{ "handsFree": false, 
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

    for warehouse in [225]:
        sql = """  
                insert into settings (value, target_type, target_id) values ('{0}', 'warehouse', {1}) """.format(jkt_json, warehouse)
        op.execute(sql)

def downgrade():
    pass
