"""remove_looker_role_and_map_to_looker_ergo

Revision ID: d1afca2d2c01
Revises: 2dec19f9f0f0
Create Date: 2021-12-06 09:43:42.808714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1afca2d2c01'
down_revision = '2dec19f9f0f0'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        DELETE FROM pipeline.casbin_rule
        WHERE v0 = 'looker'
    """)

    op.execute("""
        DELETE FROM pipeline.user_role_association
        WHERE role = 'looker' AND external_admin_user_id IN (
            SELECT * FROM (
                SELECT lookerUser.external_admin_user_id
                FROM pipeline.user_role_association as lookerUser, pipeline.user_role_association as ergoUser
                WHERE
                    lookerUser.external_admin_user_id = ergoUser.external_admin_user_id AND
                    lookerUser.role = 'looker' AND
                    ergoUser.role = 'looker_ergo'
            ) tblTmp
        )
    """)

    op.execute("""
        UPDATE pipeline.user_role_association
        SET role = 'looker_ergo'
        WHERE role = 'looker'
    """)


def downgrade():
    op.execute("""
        INSERT INTO pipeline.casbin_rule (ptype, v0, v1, v2)
        VALUES
            ('p', 'looker', 'looker', 'get'),
            ('p', 'looker', 'looker', 'post'),
            ('p', 'looker', 'looker', 'put'),
            ('p', 'looker', 'looker', 'delete')
    """)

    op.execute("""
        INSERT INTO pipeline.user_role_association (external_admin_user_id, role, db_created_at, db_modified_at)
        SELECT
            external_admin_user_id,
            'looker',
            date_format(current_timestamp(), '%Y-%m-%d %H:%i:%s'),
            date_format(current_timestamp(), '%Y-%m-%d %H:%i:%s')
        FROM (
            SELECT external_admin_user_id
            FROM pipeline.user_role_association
            WHERE role = 'looker_ergo'
        ) tblTmp
    """)
