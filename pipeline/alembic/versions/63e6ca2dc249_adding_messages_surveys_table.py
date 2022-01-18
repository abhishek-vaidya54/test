"""adding messages_surveys table

Revision ID: 63e6ca2dc249
Revises: acfc7b5ba512
Create Date: 2018-09-10 12:11:53.450459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "63e6ca2dc249"
down_revision = "acfc7b5ba512"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "messages_surveys",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("engagement", sa.String(length=30), nullable=False),
        sa.Column("days_worn", sa.Integer(), nullable=False),
        sa.Column("modal_type", sa.String(length=50), nullable=False),
        sa.Column("content", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_unique_constraint(
        "uq_eng_days_worn", "messages_surveys", ["engagement", "days_worn"]
    )


def downgrade():
    op.drop_table("messages_surveys")
    op.drop_constraint("uq_eng_days_worn", "messages_surveys")
