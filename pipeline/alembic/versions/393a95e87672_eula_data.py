"""eula-data

Revision ID: 393a95e87672
Revises: 606fd41dcb5d
Create Date: 2018-10-19 12:12:31.048008

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = "393a95e87672"
down_revision = "606fd41dcb5d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "eula",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("agreement", sa.Text(), nullable=False),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("eula")
