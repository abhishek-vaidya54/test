from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import validates, fields, ValidationError, Schema, post_dump
from datetime import datetime

from sat_orm.dockv5_orm.dock_phase import DockPhase, Config


def convert_date(date_input):
    return datetime.strptime(str(date_input), "%Y-%m-%d %H:%M:%S").strftime("%m/%d/%Y")


class DockPhaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DockPhase
        include_fk = True
        load_instance = True


class ConfigSchema(SQLAlchemyAutoSchema):
    phase = fields.Function(lambda obj: obj.phase if obj.phase else None)

    class Meta:
        model = Config
        include_fk = True
        load_instance = True
