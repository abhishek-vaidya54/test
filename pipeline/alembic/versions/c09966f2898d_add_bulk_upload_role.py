"""add bulk_upload role

Revision ID: c09966f2898d
Revises: 829cef4e1165
Create Date: 2020-12-28 12:17:29.637811

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "c09966f2898d"
down_revision = "829cef4e1165"
branch_labels = None
depends_on = None

actions = ["get", "put", "post", "delete"]


def upgrade():

    op.execute('DELETE FROM pipeline.casbin_rule where v1="bulkupload"')

    op.execute(
        'UPDATE pipeline.external_admin_user SET role="bulk_upload" where role="superuser"'
    )
    op.execute(
        'UPDATE pipeline.user_role_association SET role="bulk_upload" where role="superuser"'
    )

    op.execute(
        """
            INSERT INTO pipeline.casbin_rule (ptype, v0, v1, v2)
            SELECT ptype, "bulk_upload", v1, v2
            from pipeline.casbin_rule
            where v0="superuser"
        """
    )

    for action in actions:
        op.execute(
            'INSERT INTO pipeline.casbin_rule (ptype, v0, v1, v2) VALUES ("p", "bulk_upload", "bulkupload", "{}")'.format(
                action
            )
        )


def downgrade():
    op.execute('DELETE FROM pipeline.casbin_rule WHERE v0="bulk_upload"')
    op.execute(
        'UPDATE pipeline.external_admin_user SET role="superuser" where role="bulk_upload"'
    )
    op.execute(
        'UPDATE pipeline.user_role_association SET role="superuser" where role="bulk_upload"'
    )
    for action in actions:
        op.execute(
            'INSERT INTO pipeline.casbin_rule (ptype, v0, v1, v2) VALUES ("p", "superuser", "bulk_upload", "{}")'.format(
                action
            )
        )
