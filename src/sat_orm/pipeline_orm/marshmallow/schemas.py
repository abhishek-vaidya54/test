from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import validates, fields, ValidationError, Schema, post_dump
from datetime import datetime

from sat_orm.pipeline_orm.industrial_athlete import IndustrialAthlete
from sat_orm.pipeline_orm.client import Client
from sat_orm.pipeline_orm.warehouse import Warehouse
from sat_orm.pipeline_orm.job_function import JobFunction
from sat_orm.pipeline_orm.settings import Setting
from sat_orm.pipeline_orm.shifts import Shifts
from sat_orm.pipeline_orm.casbin_rule import CasbinRule
from sat_orm.pipeline_orm.external_admin_user import ExternalAdminUser
from sat_orm.pipeline_orm.groups import Groups
from sat_orm.pipeline_orm.user_warehouse_association import UserWarehouseAssociation
from sat_orm.pipeline_orm.user_role_association import UserRoleAssociation
from sat_orm.pipeline_orm.user_client_association import UserClientAssociation
from sat_orm.pipeline_orm.notification import Notification


def convert_date(date_input):
    try:
        converted = datetime.strptime(str(date_input), "%Y-%m-%d %H:%M:%S").strftime(
            "%m/%d/%Y"
        )
        return converted
    except:
        return ""


def convert_time(date_input):
    try:
        converted = datetime.strptime(str(date_input), "%Y-%m-%d %H:%M:%S").strftime(
            "%H:%M:%S"
        )
        return converted
    except:
        return ""


def convert_date_time(date_input):
    try:
        converted = datetime.strptime(str(date_input), "%Y-%m-%d %H:%M:%S").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return converted
    except:
        return ""


class SettingSchema(SQLAlchemyAutoSchema):
    db_created_at = fields.Function(
        lambda obj: convert_date_time(obj.db_created_at) if obj.db_created_at else None
    )

    class Meta:
        model = Setting
        include_relationships = True
        load_instance = True


class ClientSchema(SQLAlchemyAutoSchema):
    active_inactive_date = fields.Function(
        lambda obj: convert_date(obj.active_inactive_date)
        if obj.active_inactive_date
        else None
    )

    class Meta:
        model = Client
        include_relationships = True
        load_instance = True


class WarehouseSchema(SQLAlchemyAutoSchema):
    client = fields.Nested(ClientSchema(only=("id", "name")))
    client_id = fields.Function(lambda obj: obj.client.id)
    timezone = fields.Function(lambda obj: obj.prefered_timezone)

    class Meta:
        model = Warehouse
        include_relationships = True
        load_instance = True


class ShiftsSchema(SQLAlchemyAutoSchema):
    warehouse = fields.Nested(
        WarehouseSchema(only=("id", "name", "client", "timezone"))
    )
    shift_start = fields.Function(
        lambda obj: convert_time(obj.shift_start) if obj.shift_start else None
    )
    shift_end = fields.Function(
        lambda obj: convert_time(obj.shift_end) if obj.shift_end else None
    )

    class Meta:
        model = Shifts
        include_fk = True
        include_relationships = True
        load_instance = True


class JobFunctionSchema(SQLAlchemyAutoSchema):
    warehouse = fields.Nested(WarehouseSchema(only=("id", "name", "client")))
    warehouse_id = fields.Function(
        lambda obj: obj.warehouse.id if obj.warehouse else None
    )
    settings_id = fields.Function(lambda obj: obj.settings.id if obj.settings else None)

    class Meta:
        model = JobFunction
        include_relationships = True
        load_instance = True


class CasbinRuleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CasbinRule
        include_relationships = True
        load_instance = True


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


class IndustrialAthleteSchema(SQLAlchemyAutoSchema):
    warehouse = fields.Nested(WarehouseSchema(only=("id", "name")))
    shifts = fields.Nested(ShiftsSchema(only=("id", "name")))
    job_function = fields.Nested(JobFunctionSchema(only=("id", "name")))
    client = fields.Nested(ClientSchema(only=("id", "name")))

    firstName = fields.Function(lambda obj: obj.first_name)
    lastName = fields.Function(lambda obj: obj.last_name)
    externalId = fields.Function(lambda obj: obj.external_id)
    sex = fields.Function(lambda obj: obj.gender)
    clientId = fields.Function(lambda obj: obj.client.id)
    warehouseId = fields.Function(lambda obj: obj.warehouse_id)
    shiftId = fields.Function(lambda obj: obj.shift_id)
    shift = fields.Function(lambda obj: obj.shifts.name if obj.shifts else None)
    jobFunctionId = fields.Function(lambda obj: obj.job_function_id)
    jobFunction = fields.Function(
        lambda obj: obj.job_function.name if obj.job_function else None
    )
    hireDate = fields.Function(
        lambda obj: convert_date(obj.hire_date) if obj.hire_date else None
    )
    terminationDate = fields.Function(
        lambda obj: convert_date(obj.termination_date) if obj.termination_date else None
    )
    lastModified = fields.Function(
        lambda obj: convert_date(obj.db_modified_at) if obj.db_modified_at else None
    )

    @post_dump(pass_many=True)
    def add_fields(self, data, many, **kwargs):
        for key in ("client", "warehouse"):
            if key in data:
                data[key] = data[key]["name"] if data.get(key) else None

        return data

    class Meta:
        model = IndustrialAthlete
        include_fk = True
        include_relationships = True
        load_instance = True


class UserWarehouseAssociationSchema(SQLAlchemyAutoSchema):
    warehouse = fields.Nested(WarehouseSchema(only=("id", "name")))

    class Meta:
        model = UserWarehouseAssociation
        include_fk = True
        include_relationships = True
        load_instance = True


class UserRoleAssociationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserRoleAssociation
        include_fk = True
        include_relationships = True
        load_instance = True


class UserClientAssociationSchema(SQLAlchemyAutoSchema):
    client = fields.Nested(WarehouseSchema(only=("id", "name")))

    class Meta:
        model = UserClientAssociation
        include_fk = True
        include_relationships = True
        load_instance = True


class ExternalAdminUserSchema(SQLAlchemyAutoSchema):
    warehouses = fields.Nested(
        UserWarehouseAssociationSchema(only=("warehouse",)), many=True
    )
    roles = fields.Nested(UserRoleAssociationSchema(only=("role",)), many=True)
    clients = fields.Nested(UserClientAssociationSchema(only=("client",)), many=True)

    @post_dump(pass_many=True)
    def unwind_warehouses(self, data, many, **kwargs):
        to_be_modified = {
            "warehouses": "warehouse",
            "roles": "role",
            "clients": "client",
        }
        for key, value in to_be_modified.items():
            if key in data:
                data[key] = [obj.get(value) for obj in data.get(key)]

        return data

    class Meta:
        model = ExternalAdminUser
        include_fk = True
        include_relationships = True
        load_instance = True


class GroupSchema(SQLAlchemyAutoSchema):
    override_settings = fields.Function(lambda obj: bool(obj.override_settings))

    class Meta:
        model = Groups
        include_fk = True
        include_relationships = True
        load_instance = True


class NotificationSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Notification
        include_fk = True
        # include_relationships = True
        load_instance = True

