from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, ModelSchema
from marshmallow import validates, fields, ValidationError, Schema, post_dump
from datetime import datetime

from sat_orm.dockv5_orm.dock_phase import DockPhase


def convert_date(date_input):
    return datetime.strptime(str(date_input), "%Y-%m-%d %H:%M:%S").strftime("%m/%d/%Y")


class DockPhaseSchema(SQLAlchemyAutoSchema):
    phase_date = fields.Function(
        lambda obj: convert_date(obj.phase_date) if obj.phase_date else None
    )

    class Meta:
        model = DockPhase
        include_fk = True
        load_instance = True
