"""add columns gender_change_date, job_function_change_date

Revision ID: 70dbc5719915
Revises: f4daaa2c2953
Create Date: 2019-08-21 14:45:10.502486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70dbc5719915'
down_revision = 'f4daaa2c2953'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('industrial_athlete', sa.Column('gender_change_date', sa.DateTime))
    op.add_column('industrial_athlete', sa.Column('job_function_change_date', sa.DateTime))


def downgrade():
    op.drop_column('industrial_athlete','gender_change_date')
    op.drop_column('industrial_athlete','job_function_change_date')
