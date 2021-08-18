"""wastepro_update

Revision ID: 5a6ca826c31f
Revises: 1d95f47f481e
Create Date: 2021-07-08 15:31:29.838495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a6ca826c31f'
down_revision = '1d95f47f481e'
branch_labels = None
depends_on = None


def upgrade():
    wastepro_settings = """{ "handsFree": false,
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
        """.format(wastepro_settings, warehouse)
        op.execute(sql)


def downgrade():
    pass
