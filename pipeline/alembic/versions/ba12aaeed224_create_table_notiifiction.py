"""Create_table_notiifiction

Revision ID: ba12aaeed224
Revises: 4a9c7a8483d9
Create Date: 2021-12-27 18:31:34.296402

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = 'ba12aaeed224'
down_revision = '4a9c7a8483d9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('notification',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('title',sa.String(150), nullable=False),
        sa.Column('description',sa.VARCHAR(255), nullable=False),
        sa.Column('type',
            sa.Enum("update", "news", "warning", "event"),
            nullable=False,
            default="JPEG",
        ),
        sa.Column('url',sa.String(255), nullable=False),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('external_admin_user.id'), nullable=False),
        sa.Column('is_active',sa.Boolean(), nullable=True, default=False),
        sa.Column('db_created_at',sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False),
        sa.Column('db_modified_at',sa.DateTime,
            default=datetime.datetime.utcnow,
            onupdate=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('notification')

