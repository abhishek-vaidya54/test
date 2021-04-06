"""primoris

Revision ID: 247eb16e1856
Revises: 86bc75340eb7
Create Date: 2021-03-31 09:25:19.613774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '247eb16e1856'
down_revision = '624f2cb83417'
branch_labels = None
depends_on = None

def upgrade():
    op.execute(
        """
        insert into settings (value, target_type, target_id) values ('{"handsFree": false, "eulaVersion": null, "enableMotion": true, "hapticEnabled": true, "athleteEnabled": true, "showEngagement": true, "enableProximity": false, "showHapticModal": true, "enagementEnabled": true, "hapticBendNumber": 3, "enableTemperature": true, "exposureRSSILimit": -48, "hapticFeedbackGap": 0, "showBaselineModal": false, "showSafetyJudgement": true, "hapticBendPercentile": 50, "hapticFeedbackWindow": 600000, "showSafetyScoreModal": true, "exposureHapticEnabled": false, "exposureHapticRepeatMS": 10000, "hapticSingleBendWindow": 600, "hapticSagAngleThreshold": 60, "exposureHapticSuppressMS": 30000}', 'warehouse', 237)
        """
    )

    op.execute(
        """
            insert into settings (value, target_type, target_id) values ('{"handsFree": false, "eulaVersion": null, "enableMotion": true, "hapticEnabled": true, "athleteEnabled": true, "showEngagement": true, "enableProximity": false, "showHapticModal": true, "enagementEnabled": true, "hapticBendNumber": 5, "enableTemperature": true, "exposureRSSILimit": -48, "hapticFeedbackGap": 0, "showBaselineModal": false, "showSafetyJudgement": true, "hapticBendPercentile": 50, "hapticFeedbackWindow": 499800, "showSafetyScoreModal": true, "exposureHapticEnabled": false, "exposureHapticRepeatMS": 10000, "hapticSingleBendWindow": 600, "hapticSagAngleThreshold": 55, "exposureHapticSuppressMS": 30000}', 'warehouse', 238)
        """
    )

def downgrade():
      op.execute(
        """
           update industrial_athlete set group_id = Null  where warehouse_id in
            (237, 238)
        """
    )

    op.execute(
        """
            delete from settings  where id  = 1522
        """
    )

    op.execute(
        """
            delete from settings  where id  = 1523
        """
    )