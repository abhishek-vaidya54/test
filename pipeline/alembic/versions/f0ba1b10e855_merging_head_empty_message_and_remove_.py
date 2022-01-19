"""Merging head empty message and remove looker

Revision ID: f0ba1b10e855
Revises: 5639dfe3f777, d1afca2d2c01
Create Date: 2021-12-09 10:09:26.120793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f0ba1b10e855"
down_revision = ("5639dfe3f777", "d1afca2d2c01")
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
