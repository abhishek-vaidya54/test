"""create & populate user_role_association table

Revision ID: 829cef4e1165
Revises: dfc30fb88fee
Create Date: 2020-12-24 18:17:02.431317

"""
import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

# revision identifiers, used by Alembic.
revision = "829cef4e1165"
down_revision = "dfc30fb88fee"
branch_labels = None
depends_on = None

Base = declarative_base()


class UserRoleAssociation(Base):
    __tablename__ = "user_role_association"

    external_admin_user_id = sa.Column(sa.Integer, nullable=False, primary_key=True)
    role = sa.Column(sa.String(30), nullable=False, default="manager", primary_key=True)
    db_created_at = sa.Column(
        sa.DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    db_modified_at = sa.Column(
        sa.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )


def upgrade():
    op.create_table(
        "user_role_association",
        sa.Column(
            "external_admin_user_id", sa.Integer(), nullable=False, primary_key=True
        ),
        sa.Column("role", sa.String(length=30), nullable=False, primary_key=True),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.Column(
            "db_modified_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["external_admin_user_id"],
            ["external_admin_user.id"],
            name="fk_user_role_assoc_external_admin_user",
        ),
    )

    bind = op.get_bind()
    session = orm.Session(bind=bind)
    existing_records = session.execute(
        "SELECT id, role FROM external_admin_user"
    ).fetchall()

    new_records = [
        UserRoleAssociation(external_admin_user_id=record.id, role=record.role)
        for record in existing_records
    ]

    session.add_all(new_records)
    session.commit()
    session.close()


def downgrade():
    op.drop_table("user_role_association")
