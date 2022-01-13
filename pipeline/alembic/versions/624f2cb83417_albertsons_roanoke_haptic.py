"""albertsons_roanoke_haptic

Revision ID: 624f2cb83417
Revises: f7e1e02708e5
Create Date: 2021-04-02 09:31:53.556730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "624f2cb83417"
down_revision = "ac32b3b8ec9d"
branch_labels = None
depends_on = None


def upgrade():

    op.execute(
        """

           update industrial_athlete set group_id = 204  where warehouse_id in

               (220)

       """
    )

    op.execute(
        """

insert into settings (value, target_type, target_id) values ('{"handsFree": false, "eulaVersion": null, "enableMotion": true, "hapticEnabled": true, "athleteEnabled": true, "showEngagement": true, "enableProximity": false, "showHapticModal": true, "enagementEnabled": true, "hapticBendNumber": 3, "enableTemperature": true, "exposureRSSILimit": -48, "hapticFeedbackGap": 0, "showBaselineModal": false, "showSafetyJudgement": true, "hapticBendPercentile": 50, "hapticFeedbackWindow": 300000, "showSafetyScoreModal": true, "exposureHapticEnabled": false, "exposureHapticRepeatMS": 10000, "hapticSingleBendWindow": 600, "hapticSagAngleThreshold": 70, "exposureHapticSuppressMS": 30000}', 'warehouse', 204)

       """
    )


def downgrade():
    pass
