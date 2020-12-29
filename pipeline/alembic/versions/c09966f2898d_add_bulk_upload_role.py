"""add bulk_upload role

Revision ID: c09966f2898d
Revises: dfc30fb88fee
Create Date: 2020-12-28 12:17:29.637811

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base


# revision identifiers, used by Alembic.
revision = 'c09966f2898d'
down_revision = 'dfc30fb88fee'
branch_labels = None
depends_on = None

actions = ['get', 'put', 'post', 'delete']

def upgrade():

    op.execute('DELETE FROM pipeline.casbin_rule where v1="bulkupload"')

    op.execute('UPDATE pipeline.external_admin_user SET role="bulk_upload" where role="admin" or role="superuser"')

    op.execute('''INSERT INTO pipeline.casbin_rule (ptype, v0, v1, v2) 
        SELECT ptype, "bulk_upload", v1, v2
        from pipeline.casbin_rule
        where v0="superuser"''')

    for action in actions:
        op.execute('INSERT INTO pipeline.casbin_rule (ptype, v0, v1, v2) VALUES ("p", "bulk_upload", "bulkupload", "{}")'.format(action))

    pass


def downgrade():
    op.execute('DELETE FROM pieline.casbin_rule WHERE v0="bulk_upload"')
    op.execute('UPDATE pipeline.external_admin_user SET role="admin" where role="bulk_upload""')
    for action in actions:
        op.execute('INSERT INTO pipeline.casbin_rule (ptype, v0, v1, v2) VALUES "p", "admin", "bulk_upload", "{}"'.format(action))
    pass
