"""add foreign key constraints for admin dashboard tables

Revision ID: 5ebe016d83da
Revises: bd409c6a307d
Create Date: 2019-06-26 14:38:37.100634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ebe016d83da'
down_revision = 'bd409c6a307d'
branch_labels = None
depends_on = None


def upgrade():
    # Set NULL all hire_date = "0000-00-00 00:00:00", prevented adding foreign keys
    op.execute("""
        UPDATE pipeline.industrial_athlete SET hire_date = NULL
        WHERE CAST(hire_date AS CHAR(20)) = "0000-00-00 00:00:00";
    """)
    # Add foreign key constraint from industrial_athlete.client_id to client.id
    op.create_foreign_key(
            "fk_ia_client",
            "industrial_athlete", "client",
            ["client_id"], ["id"])

    # Set NULL all warehouse_id that violate warehouse foreign key
    op.execute("""
        UPDATE industrial_athlete ia
        LEFT OUTER JOIN warehouse w ON ia.warehouse_id = w.id
        SET ia.warehouse_id = NULL
        WHERE w.id IS NULL;
    """)
    # Add foreign key constraint from industrial_athlete.warehouse_id to warehouse.id
    op.create_foreign_key(
            "fk_ia_warehouse",
            "industrial_athlete", "warehouse",
            ["warehouse_id"], ["id"])

    # Set NULL all shift_id that violate shifts foreign key
    op.execute("""
        UPDATE industrial_athlete ia
        LEFT OUTER JOIN shifts s ON ia.shift_id = s.id
        SET ia.shift_id = NULL
        WHERE s.id IS NULL;
    """)
    # Add foreign key constraint from industrial_athlete.shift_id to shifts.id
    op.create_foreign_key(
            "fk_ia_shifts",
            "industrial_athlete", "shifts",
            ["shift_id"], ["id"])

    # Set NULL all job_function_id that violate job_function foreign key
    op.execute("""
        UPDATE industrial_athlete ia
        LEFT OUTER JOIN job_function jf ON ia.job_function_id = jf.id
        SET ia.job_function_id = NULL
        WHERE jf.id IS NULL;
    """)
    # Add foreign key constraint from industrial_athlete.job_function_id to job_function.id
    op.create_foreign_key(
            "fk_ia_job_function",
            "industrial_athlete", "job_function",
            ["job_function_id"], ["id"])

    # Set NULL all group_id that violate group foreign key
    op.execute("""
        UPDATE industrial_athlete ia
        LEFT OUTER JOIN groups g ON ia.group_id = g.id
        SET ia.group_id = NULL
        WHERE g.id IS NULL;
    """)
    # Add foreign key constraint from industrial_athlete.group_id to group.id
    op.create_foreign_key(
            "fk_ia_groups",
            "industrial_athlete", "groups",
            ["group_id"], ["id"])

    # Set NULL all setting_id that violate setting foreign key
    op.execute("""
        UPDATE industrial_athlete ia
        LEFT OUTER JOIN settings se ON ia.setting_id = se.id
        SET ia.setting_id = NULL
        WHERE se.id IS NULL;
    """)
    # Add foreign key constraint from industrial_athlete.setting_id to setting.id
    op.create_foreign_key(
            "fk_ia_settings",
            "industrial_athlete", "settings",
            ["setting_id"], ["id"])

def downgrade():
    op.drop_constraint("fk_ia_client", "industrial_athlete", "foreignkey")
    op.drop_constraint("fk_ia_warehouse", "industrial_athlete", "foreignkey")
    op.drop_constraint("fk_ia_shifts", "industrial_athlete", "foreignkey")
    op.drop_constraint("fk_ia_job_function", "industrial_athlete", "foreignkey")
    op.drop_constraint("fk_ia_groups", "industrial_athlete", "foreignkey")
    op.drop_constraint("fk_ia_settings", "industrial_athlete", "foreignkey")
