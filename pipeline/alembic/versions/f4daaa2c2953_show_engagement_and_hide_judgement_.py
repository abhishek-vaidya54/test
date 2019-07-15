"""show_engagement and hide_judgement removed from warehouse table and added to settings blob

Revision ID: f4daaa2c2953
Revises: 5ebe016d83da
Create Date: 2019-07-09 12:44:55.057322

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TINYINT
import json
import datetime

Base = declarative_base()

# revision identifiers, used by Alembic.
revision = 'f4daaa2c2953'
down_revision = '5ebe016d83da'
branch_labels = None
depends_on = None

class Warehouse(Base):
    __tablename__ = 'warehouse'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    show_engagement = sa.Column(TINYINT, nullable=False)
    hide_judgement = sa.Column(TINYINT, nullable=False)

class Settings(Base):
    __tablename__ = 'settings'
    
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    target_id = sa.Column(sa.Integer, nullable=False)
    target_type = sa.Column(sa.Text, nullable=False)

    value = sa.Column(sa.JSON)
  
    db_created_at = sa.Column(
        sa.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )

def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    


def downgrade():
    pass
