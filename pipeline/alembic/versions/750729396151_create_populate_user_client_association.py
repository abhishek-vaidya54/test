"""create_populate_user_client_association

Revision ID: 750729396151
Revises: 0dfec63dee9c
Create Date: 2021-01-29 15:18:11.443185

"""
import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

# revision identifiers, used by Alembic.
revision = "750729396151"
down_revision = "0dfec63dee9c"
branch_labels = None
depends_on = None


Base = declarative_base()


class UserClientAssociation(Base):
    __tablename__ = "user_client_association"

    external_admin_user_id = sa.Column(sa.Integer, nullable=False, primary_key=True)
    client_id = sa.Column(sa.Integer(), nullable=False, primary_key=True)
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
        "user_client_association",
        sa.Column(
            "external_admin_user_id", sa.Integer(), nullable=False, primary_key=True
        ),
        sa.Column("client_id", sa.Integer(), nullable=False, primary_key=True),
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
            name="fk_user_client_assoc_external_admin_user",
        ),
    )

    bind = op.get_bind()
    session = orm.Session(bind=bind)
    existing_records = session.execute(
        "SELECT id, client_id FROM external_admin_user"
    ).fetchall()

    new_records = [
        UserClientAssociation(
            external_admin_user_id=record.id, client_id=record.client_id
        )
        for record in existing_records
    ]

    session.add_all(new_records)
    session.commit()

    client_id_index = session.execute(
        """
            SHOW INDEXES FROM external_admin_user
            WHERE key_name='fk_ext_admin_user_client'
        """
    ).fetchone()
    session.close()

    if client_id_index:
        op.drop_constraint(
            "fk_ext_admin_user_client", "external_admin_user", "foreignkey"
        )

    op.drop_column("external_admin_user", "client_id")


def downgrade():
    op.add_column(
        "external_admin_user",
        sa.Column("client_id", sa.Integer(), nullable=False, server_default="33"),
    )
    op.create_foreign_key(
        "fk_ext_admin_user_client",
        "external_admin_user",
        "client",
        ["client_id"],
        ["id"],
    )

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    users = session.execute(
        """
            SELECT u.id, uca.client_id FROM external_admin_user u
            INNER JOIN user_client_association uca
            ON (u.id = uca.external_admin_user_id)
        """
    )

    for user in users:
        session.execute(
            f"UPDATE external_admin_user SET client_id={user.client_id} WHERE id={user.id}"
        )

    session.commit()
    session.close()

    op.drop_table("user_client_association")