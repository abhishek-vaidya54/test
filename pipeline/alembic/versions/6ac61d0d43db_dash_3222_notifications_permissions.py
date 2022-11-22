"""dash_3222_notifications_permissions

Revision ID: 6ac61d0d43db
Revises: 6bdad663e8ef
Create Date: 2022-10-26 08:15:13.938466

"""
from alembic import op
from sqlalchemy import orm


# revision identifiers, used by Alembic.
revision = "6ac61d0d43db"
down_revision = "6bdad663e8ef"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.execute(
        """
        DELETE FROM pipeline.casbin_rule
        WHERE v1 = 'notifications' AND v2 = 'get' AND ptype='p';
    """
    )
    session.execute(
        """
        INSERT INTO pipeline.casbin_rule (ptype, v0, v1, v2)
	    VALUES  ('p', 'looker_ergo', 'notifications', 'get'),
                ('p', 'superuser', 'notifications', 'get'),
                ('p', 'shift_manager', 'notifications', 'get'),
                ('p', 'admin', 'notifications', 'get'),
                ('p', 'manager', 'notifications', 'get'),
                ('p', 'looker_prox', 'notifications', 'get'),
                ('p', 'bulk_upload', 'notifications', 'get'),
                ('p', 'analytics_heatstress', 'notifications', 'get');
        """
    )
    session.commit()
    session.close()


def downgrade():
    op.execute(
        """
        DELETE FROM pipeline.casbin_rule
        WHERE v0<>'superuser' AND  v1 = 'notifications' 
                              AND v2 = 'get' AND ptype='p';
        """
    )
