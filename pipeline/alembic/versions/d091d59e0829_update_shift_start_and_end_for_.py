"""update_shift_start_and_end_for_clickhouse_upgrade

Revision ID: d091d59e0829
Revises: b48b02b5fcef
Create Date: 2022-05-25 21:19:45.490135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d091d59e0829"
down_revision = "b48b02b5fcef"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            UPDATE pipeline.shifts
            SET
                shift_start = STR_TO_DATE(
                    CONCAT('1970-01-01 ', DATE_FORMAT(shift_start, "%H:%i:%s")),
                    '%Y-%m-%d %H:%i:%s'
                ),
                shift_end = STR_TO_DATE(
                    CONCAT('1970-01-01 ', DATE_FORMAT(shift_end, "%H:%i:%s")),
                    '%Y-%m-%d %H:%i:%s'
                )
            WHERE DATE(shift_start) = DATE('1900-01-01') OR DATE(shift_end) = DATE('1900-01-01')
        """
    )


def downgrade():
    op.execute(
        """
            UPDATE pipeline.shifts
            SET
                shift_start = STR_TO_DATE(
                    CONCAT('1900-01-01 ', DATE_FORMAT(shift_start, "%H:%i:%s")),
                    '%Y-%m-%d %H:%i:%s'
                ),
                shift_end = STR_TO_DATE(
                    CONCAT('1900-01-01 ', DATE_FORMAT(shift_end, "%H:%i:%s")),
                    '%Y-%m-%d %H:%i:%s'
                )
            WHERE DATE(shift_start) = DATE('1970-01-01') OR DATE(shift_end) = DATE('1970-01-01')
        """
    )
