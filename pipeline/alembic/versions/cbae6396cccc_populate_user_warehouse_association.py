"""populate user warehouse association

Revision ID: cbae6396cccc
Revises: 61bb059d421a
Create Date: 2020-12-07 16:40:04.626174

"""
import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.exc import InternalError

Base = declarative_base()


# revision identifiers, used by Alembic.
revision = 'cbae6396cccc'
down_revision = '61bb059d421a'
branch_labels = None
depends_on = None

class UserWarehouseAssociation(Base):
    __tablename__ = "user_warehouse_association"

    external_admin_user_id = sa.Column(sa.Integer, primary_key=True)
    warehouse_id = sa.Column(sa.Integer, primary_key=True)

    db_created_at = sa.Column(
        sa.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False)
    db_modified_at = sa.Column(
        sa.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )



def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    res = session.execute("SELECT id, warehouse_id FROM external_admin_user")

    
    existing_records = res.fetchall()
    new_records = []

    # try:
    for record in existing_records:
        new_records.append(
            UserWarehouseAssociation(
                external_admin_user_id=record.id,
                warehouse_id=record.warehouse_id)
        )
    # finally:
    session.add_all(new_records)
    session.commit()
    session.close()
            


def downgrade():
    op.execute(
        """
        DELETE FROM user_warehouse_association
        """
    )
