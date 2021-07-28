"""primoris_newwarehouse_haptic

Revision ID: c98b2ed86844
Revises: ff8fcda90104
Create Date: 2021-05-21 14:44:15.562036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c98b2ed86844'
down_revision = 'ff8fcda90104'
branch_labels = None
depends_on = None


def upgrade():
    primoris_settings_json = """{ "handsFree": false,
                "eulaVersion": null,
                "enableMotion": true,
                "hapticEnabled": false,
                "athleteEnabled": false,
                "showEngagement": true,
                "enableProximity": true,
                "showHapticModal": false,
                "enagementEnabled": true,
                "hapticBendNumber": 1,
                "enableTemperature": true,
                "exposureRSSILimit": -48,
                "hapticFeedbackGap": 0,
                "showBaselineModal": true,
                "showSafetyJudgement": true,
                "hapticBendPercentile": 50,
                "hapticFeedbackWindow": 0,
                "showSafetyScoreModal": true,
                "exposureHapticEnabled": false,
                "exposureHapticRepeatMS": 10000,
                "hapticSingleBendWindow": 600,
                "hapticSagAngleThreshold": 70,
                "exposureHapticSuppressMS": 30000}""".replace('\n', '')

    for warehouse in [270]:
        sql = """
            insert into settings (value, target_type, target_id)
            values ('{0}',
                'warehouse', {1})
        """.format(primoris_settings_json, warehouse)
        op.execute(sql)


def downgrade():
    pass
