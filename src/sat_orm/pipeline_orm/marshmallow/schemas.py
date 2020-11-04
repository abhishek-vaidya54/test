from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, ModelSchema
from marshmallow import validates, fields, ValidationError, Schema, post_dump

from sat_orm.pipeline_orm.industrial_athlete import IndustrialAthlete
from sat_orm.pipeline_orm.client import Client
from sat_orm.pipeline_orm.warehouse import Warehouse
from sat_orm.pipeline_orm.job_function import JobFunction
from sat_orm.pipeline_orm.settings import Setting
from sat_orm.pipeline_orm.shifts import Shifts


# class ShiftsSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Shifts
#         include_relationships = True
#         load_instance = True


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


# class IndustrialAthleteSchema(ModelSchema):
#     hire_date = CustomDateField()
#     first_name = fields.Str(load_only=False)
#     # client_id = fields.Nested(ClientSchema)
#     # warehouse_id = fields.Nested(WarehouseSchema)
#     # job_function_id = fields.Nested(JobFunctionSchema)
#     # shift_id = fields.Nested(ShiftsSchema, load_from='shiftId')
#     # shift_id = fields.Str(load_from='shiftId')
#     class Meta:
#         model = IndustrialAthlete
#         include_fk = True
#         # include_relationships = True
#         extend_existing = True

#     # @pre_load
#     # def set_field_session(self, data, **kwargs):
#     #     for value in filter(lambda f: hasattr(f, 'schema'), self.fields.values()):
#     #         value.schema.session = self.session
#     @validates("hire_date")
#     def validate_hire_date(self, value):
#         print("HIRE_DATE ===>", value)

#     @validates("first_name")
#     def validate_first_name(self, value):
#         print("VALIDATING ===>", value)
#         if value == "Mukul":
#             raise ValidationError("Cannot be Mukul")