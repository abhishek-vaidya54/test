"""dropping deprecated columns from client table

Revision ID: aa5e10e70123
Revises: 393a95e87672
Create Date: 2018-11-26 10:21:19.793938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "aa5e10e70123"
down_revision = "393a95e87672"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("client", "guid")
    op.drop_column("client", "domain")
    op.drop_column("client", "client_regex_code")
    op.drop_column("client", "account_lock_timeout")
    op.drop_column("client", "dynamic_shift")
    op.drop_column("client", "algo_version")


def downgrade():
    op.add_column("client", sa.Column("guid", sa.String(length=32), nullable=True))
    op.add_column("client", sa.Column("domain", sa.String(length=255), nullable=True))
    op.add_column(
        "client", sa.Column("client_regex_code", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "client", sa.Column("account_lock_timeout", sa.Integer(), nullable=True)
    )
    op.add_column("client", sa.Column("dynamic_shift", sa.Integer(), nullable=True))
    op.add_column("client", sa.Column("algo_version", sa.Integer(), nullable=True))
