"""Merge b6978481f4b1 and deedee498933

Revision ID: e618e32273b3
Revises: deedee498933, b6978481f4b1
Create Date: 2020-12-10 18:37:18.787203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e618e32273b3"
down_revision = ("deedee498933", "b6978481f4b1")
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
