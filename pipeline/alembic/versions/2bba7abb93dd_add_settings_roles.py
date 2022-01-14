"""add_settings_roles

Revision ID: 2bba7abb93dd
Revises: 9eb6e8b682a1
Create Date: 2021-05-18 16:35:53.146488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2bba7abb93dd"
down_revision = "9eb6e8b682a1"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
    INSERT INTO pipeline.casbin_rule
        (ptype, v0, v1, v2)
    VALUES
        ("p", "admin", "settings", "get"),
        ("p", "admin", "settings", "post")

    """
    )


def downgrade():
    op.execute(
        """
    DELETE FROM pipeline.casbin_rule WHERE v0='admin' AND v1='settings';    
    """
    )
