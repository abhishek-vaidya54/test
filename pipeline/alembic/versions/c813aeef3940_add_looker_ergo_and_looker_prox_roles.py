"""add_looker_ergo_and_looker_prox_roles

Revision ID: c813aeef3940
Revises: 7362f276939c
Create Date: 2021-01-13 16:03:30.128454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c813aeef3940"
down_revision = "7362f276939c"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
    INSERT INTO pipeline.casbin_rule
        (ptype, v0, v1, v2)
    VALUES
        ("p", "looker_ergo", "looker_ergo", "get"),
        ("p", "looker_ergo", "looker_ergo", "post"),
        ("p", "looker_ergo", "looker_ergo", "put"),
        ("p", "looker_ergo", "looker_ergo", "delete"),
        ("p", "looker_prox", "looker_prox", "get"),
        ("p", "looker_prox", "looker_prox", "post"),
        ("p", "looker_prox", "looker_prox", "put"),
        ("p", "looker_prox", "looker_prox", "delete");

    """
    )


def downgrade():
    op.execute(
        """
    DELETE FROM pipeline.casbin_rule WHERE v0='looker_ergo' AND v1='looker_ergo';
    DELETE FROM pipeline.casbin_rule WHERE v0='looker_prox' AND v1='looker_prox';
    
    """
    )
