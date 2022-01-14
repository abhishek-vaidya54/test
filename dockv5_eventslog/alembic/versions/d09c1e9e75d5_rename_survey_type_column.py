"""rename_survey_type_column

Revision ID: d09c1e9e75d5
Revises: 9153ace06182
Create Date: 2019-03-28 17:50:54.118772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d09c1e9e75d5"
down_revision = "9153ace06182"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "survey_events",
        "survey_type",
        new_column_name="content_id",
        type_=sa.Unicode(length=45),
        existing_server_default=False,
        existing_nullable=True,
    )
    pass


def downgrade():
    op.alter_column(
        "survey_events",
        "content_id",
        new_column_name="survey_type",
        type_=sa.Unicode(length=45),
        existing_server_default=False,
        existing_nullable=True,
    )
    pass
