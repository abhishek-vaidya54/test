"""create table dock_phase

Revision ID: a84e5071162a
Revises: 97618bd2ecc2
Create Date: 2020-08-26 14:33:09.639953

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text, orm
from sqlalchemy.ext.declarative import declarative_base

# revision identifiers, used by Alembic.
revision = "a84e5071162a"
down_revision = "97618bd2ecc2"
branch_labels = None
depends_on = None

Base = declarative_base()


class DockPhase(Base):
    __tablename__ = "dock_phase"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    dock_id = sa.Column(sa.String(length=255), nullable=False)
    description = sa.Column(sa.String(length=255), nullable=False, default="")
    warehouse_id = sa.Column(sa.Integer, nullable=False)
    client_id = sa.Column(sa.Integer, nullable=False)
    dock_firmware = sa.Column(sa.Boolean, nullable=True, default=False)
    dock_firmware_version = sa.Column(sa.String(length=10), nullable=False)
    timestamp = sa.Column(
        sa.DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    phase = sa.Column(
        sa.Enum("DEPLOYED", "NOT DEPLOYED", "MAINTENANCE"),
        nullable=False,
        default="NOT DEPLOYED",
    )
    phase_date = sa.Column(sa.DateTime, nullable=True)
    deployment_stage = sa.Column(sa.Enum("DEV", "PROD"), nullable=False, default="dev")


def get_records(session):
    records = []
    try:
        records = [
            DockPhase(
                dock_id=dock_phase.dock_id.strip(),
                description=dock_phase.description or "",
                client_id=dock_phase.client_id,
                warehouse_id=dock_phase.warehouse_id,
                dock_firmware_version=dock_phase.dock_firmware_version,
                phase=dock_phase.phase.upper(),
                phase_date=dock_phase.phase_date,
                deployment_stage=dock_phase.deployment_stage.upper(),
            )
            for dock_phase in session.query(DockPhase).all()
        ]
    finally:
        return records


def upgrade():
    pass
    # bind = op.get_bind()
    # session = orm.Session(bind=bind)
    # records = get_records(session)

    # op.drop_table("dock_phase")
    # DockPhase.__table__.create(bind)

    # session.add_all(records)
    # session.commit()
    # session.close()


def downgrade():
    pass
