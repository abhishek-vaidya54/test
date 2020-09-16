"""update warehouse fields

Revision ID: b0d0b3c39ada
Revises: 0e25b3d033ee
Create Date: 2020-09-16 18:22:16.090158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b0d0b3c39ada"
down_revision = "0e25b3d033ee"
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.drop_column("warehouse", "number_of_user_allocated")
        op.drop_column("warehouse", "city")
        op.drop_column("warehouse", "state")
        op.drop_column("warehouse", "country")
        op.drop_column("warehouse", "industry")
        op.drop_column("warehouse", "latitude")
        op.drop_column("warehouse", "longitude")
    except:
        pass
    finally:
        op.add_column(
            "warehouse",
            sa.Column("number_of_user_allocated", sa.Integer(), nullable=True),
        )
        op.add_column(
            "warehouse",
            sa.Column("city", sa.String(length=20), nullable=True),
        )
        op.add_column(
            "warehouse",
            sa.Column("state", sa.String(length=20), nullable=True),
        )
        op.add_column(
            "warehouse",
            sa.Column("country", sa.String(length=20), nullable=True),
        )
        op.add_column(
            "warehouse",
            sa.Column("industry", sa.String(length=20), nullable=False),
        )
        op.add_column(
            "warehouse",
            sa.Column("latitude", sa.Float, nullable=True),
        )
        op.add_column(
            "warehouse",
            sa.Column("longitude", sa.Float, nullable=True),
        )
        op.add_column(
            "warehouse",
            sa.Column("lat_direction", sa.Enum("N", "S", "E", "W"), server_default="N"),
        )
        op.add_column(
            "warehouse",
            sa.Column(
                "long_direction", sa.Enum("N", "S", "E", "W"), server_default="N"
            ),
        )


def downgrade():
    op.drop_column("warehouse", "number_of_user_allocated")
    op.drop_column("warehouse", "city")
    op.drop_column("warehouse", "state")
    op.drop_column("warehouse", "country")
    op.drop_column("warehouse", "industry")
    op.drop_column("warehouse", "latitude")
    op.drop_column("warehouse", "longitude")
    op.drop_column("warehouse", "lat_direction")
    op.drop_column("warehouse", "long_direction")
