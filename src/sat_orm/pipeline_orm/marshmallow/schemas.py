from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, ModelSchema
from marshmallow import validates, fields, ValidationError, Schema, post_dump
from datetime import datetime

from sat_orm.pipeline_orm.industrial_athlete import IndustrialAthlete
from sat_orm.pipeline_orm.client import Client
from sat_orm.pipeline_orm.warehouse import Warehouse
from sat_orm.pipeline_orm.job_function import JobFunction
from sat_orm.pipeline_orm.settings import Setting
from sat_orm.pipeline_orm.shifts import Shifts


def convert_date(date_input):
    return datetime.strptime(str(date_input), "%Y-%m-%d %H:%M:%S").strftime("%m/%d/%Y")


class ShiftsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Shifts
        include_relationships = True
        load_instance = True


class SettingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Setting
        include_relationships = True
        load_instance = True


class WarehouseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Warehouse
        include_relationships = True
        load_instance = True


class JobFunctionSchema(SQLAlchemyAutoSchema):
    warehouse = fields.Nested(WarehouseSchema(only=("id", "name")))
    warehouse_id = fields.Function(lambda obj: obj.warehouse.id)
    settings_id = fields.Function(lambda obj: obj.settings.id)

    class Meta:
        model = JobFunction
        include_relationships = True
        load_instance = True


# class ClientSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Client
#         include_relationships = True
#         load_instance = True


# class CustomDateField(fields.Field):
#     def _serialize(self, value, attr, obj, **kwargs):
#         if value is None:
#             return ""
#         date_arr = value.split("-")
#         # m/d/y
#         return "{}/{}/{}".format(date_arr[1], date_arr[2], date_arr[0])

#     # def _deserialize(self, value, attr, data, **kwargs):
#     #     try:
#     #         return [int(c) for c in value]
#     #     except ValueError as error:
#     #         raise ValidationError("Pin codes must contain only digits.") from error


class IndustrialAthleteSchema(ModelSchema):
    warehouse = fields.Nested(WarehouseSchema(only=("id", "name")))
    shifts = fields.Nested(ShiftsSchema(only=("id", "name")))
    job_function = fields.Nested(JobFunctionSchema(only=("id", "name")))

    firstName = fields.Function(lambda obj: obj.first_name)
    lastName = fields.Function(lambda obj: obj.last_name)
    externalId = fields.Function(lambda obj: obj.external_id)
    sex = fields.Function(lambda obj: obj.gender)
    warehouseId = fields.Function(lambda obj: obj.warehouse_id)
    shiftId = fields.Function(lambda obj: obj.shift_id)
    jobFunctionId = fields.Function(lambda obj: obj.job_function_id)
    hireDate = fields.Function(
        lambda obj: convert_date(obj.hire_date) if obj.hire_date else None
    )
    terminationDate = fields.Function(
        lambda obj: convert_date(obj.termination_date) if obj.termination_date else None
    )

    class Meta:
        model = IndustrialAthlete
        include_fk = True
        include_relationships = True
        load_instance = True