"""map_client_portal_role_to_shift_manager

Revision ID: 4aabd584e0f5
Revises: e7338c9b18c7
Create Date: 2021-10-25 14:04:51.322627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4aabd584e0f5"
down_revision = "e7338c9b18c7"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        UPDATE pipeline.casbin_rule
        SET v0 = 'shift_manager', v1 = 'shift_manager'
        WHERE v0 = 'client-portal'
    """
    )

    op.execute(
        """
        UPDATE pipeline.user_role_association
        SET role = 'shift_manager'
        WHERE role = 'client-portal'
    """
    )


def downgrade():
    op.execute(
        """
        UPDATE pipeline.user_role_association
        SET role = 'client-portal'
        WHERE role = 'shift_manager'
    """
    )

    op.execute(
        """
        UPDATE pipeline.casbin_rule
        SET v0 = 'client-portal', v1 = 'client-portal'
        WHERE v0 = 'shift_manager'
    """
    )
