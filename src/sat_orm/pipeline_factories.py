"""
Contributor: Vincent Turnier
Date Edited: September 18th, 2019
Note:
Description:
"""
# Standard Library
import datetime
import string
import random

# Third Party Import
import factory
import factory.fuzzy
import uuid
from smalluuid import SmallUUID

# Local Application Import
from sat_orm.pipeline import (
    Client,
    IndustrialAthlete,
    JobFunction,
    Warehouse,
    Shifts,
    ExternalAdminUser,
    Setting,
    ImportedIndustrialAthlete,
    AthleteUploadStatus,
    CasbinRule,
    Sensors,
    Groups,
    UserWarehouseAssociation,
    UserRoleAssociation,
    UserClientAssociation,
)


def random_str():
    char_set = string.ascii_uppercase + string.digits
    return "".join(random.sample(char_set * 6, 6))


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Client Factory: creates a fake client with its relationships"""

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "Test Client {0}".format(random_str()))
    prefix = factory.Sequence(lambda n: n + 1)
    db_created_at = datetime.datetime.now()
    db_modified_at = datetime.datetime.now()
    enable_processing = True
    status = factory.fuzzy.FuzzyChoice(["pilot", "deployment", "rollout", "inactive"])
    contracted_users = factory.fuzzy.FuzzyInteger(1, 999999)
    active_inactive_date = datetime.datetime.now()
    ia_name_format = "ANONYMOUS"

    # @factory.post_generation
    # def warehouse(self,create,extracted, **kwargs):
    # if extracted is None:
    #     extracted = 3

    # make_warehouses = getattr(WarehouseFactory,'create' if create else 'build')
    # self.warehouses = [make_warehouses(client_id=self.id) for i in range(extracted)]
    # if not create:
    #     self._prefetched_objects_cache = {'warehouses':self.warehouses}
    class Meta:
        model = Client
        sqlalchemy_session_persistence = "commit"


class ExternalAdminUserFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    email = "email-{0}@email.com".format(random_str())
    username = str(uuid.uuid4())
    client = factory.RelatedFactory(ClientFactory)

    class Meta:
        model = ExternalAdminUser
        sqlalchemy_session_persistence = "commit"


class WarehouseFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Warehouse Factory: creates a fake warehouse with its relationships if the relationships are not None"""

    id = factory.Sequence(lambda n: n)
    client = factory.SubFactory(ClientFactory)
    name = factory.Faker("first_name")
    location = factory.Faker("address")
    db_created_at = datetime.datetime.now()
    db_modified_at = datetime.datetime.now()
    prefered_timezone = "US/Eastern"
    display_names = factory.Sequence(lambda n: n % 2)
    utc_op_day_start = "07:00"
    week_start = factory.fuzzy.FuzzyChoice(
        ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    )
    update_engagement = factory.Sequence(lambda n: n % 2)
    number_of_user_allocated = factory.fuzzy.FuzzyInteger(1, 999999)
    city = factory.fuzzy.FuzzyText(length=12)
    state = factory.fuzzy.FuzzyText(length=12)
    country = factory.fuzzy.FuzzyText(length=12)
    industry = factory.fuzzy.FuzzyText(length=20)
    latitude = factory.fuzzy.FuzzyFloat(-90, 90)
    longitude = factory.fuzzy.FuzzyFloat(-180, 180)
    lat_direction = factory.fuzzy.FuzzyChoice(["N", "S", "E", "W"])
    long_direction = factory.fuzzy.FuzzyChoice(["N", "S", "E", "W"])
    # @factory.post_generation
    # def job_functions(self,create,extracted,**kwargs):
    #     if extracted is None:
    #         extracted = 1

    #     make_job_functions = getattr(JobFunctionFactory,'create' if create else 'build')
    #     self.job_functions = [make_job_functions(warehouse_id=self.id) for i in range(extracted)]
    #     if not create:
    #         self._prefetched_objects_cache = {'job_functions':self.job_functions}

    # @factory.post_generation
    # def shifts(self,create,extracted, **kwargs):
    #     if extracted is None:
    #         extracted = 2
    #     make_shifts = getattr(ShiftsFactory,'create' if create else 'build')
    #     self.shifts = [make_shifts(warehouse_id=self.id) for i in range(extracted)]
    #     if not create:
    #         self._prefetched_objects_cache = {'shifts':self.shifts}

    # @factory.post_generation
    # def industrial_athlete(self,create,extracted, **kwargs):
    #     if extracted is None:
    #         extracted = 25

    #     make_industrial_athlete = getattr(IndustrialAthleteFactory,'create' if create else 'build')
    #     self.industrial_athletes = [make_industrial_athlete(client_id=self.client_id,
    #                                                         warehouse_id=self.id,
    #                                                         shift_id=self.shifts[0].id,
    #                                                         job_function_id=self.job_functions[0].id) for i in range(extracted)]

    class Meta:
        model = Warehouse
        sqlalchemy_session_persistence = "commit"


class ShiftsFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Shift Factory: creates a fake shift as well as any of its relationships"""

    id = factory.Sequence(lambda n: n)
    warehouse = factory.SubFactory(WarehouseFactory)
    name = factory.fuzzy.FuzzyChoice(["Shift 1", "Shift 2", "Shift 3"])
    shift_start = datetime.datetime.now()
    shift_end = datetime.datetime.now()
    db_created_at = datetime.datetime.now()
    db_modified_at = datetime.datetime.now()
    color = None
    description = factory.Faker("sentence")
    override_settings = 0
    external_admin_user = factory.SubFactory(ExternalAdminUserFactory)

    class Meta:
        model = Shifts
        sqlalchemy_session_persistence = "commit"


class SettingsFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    target_type = "warehouse"
    target_id = 53
    value = {
        "handsFree": True,
        "eulaVersion": None,
        "enableMotion": False,
        "hapticEnabled": False,
        "athleteEnabled": True,
        "showEngagement": True,
        "enableProximity": False,
        "showHapticModal": False,
        "enagementEnabled": True,
        "hapticBendNumber": 3,
        "enableTemperature": True,
        "exposureRSSILimit": -48,
        "hapticFeedbackGap": 0,
        "showBaselineModal": False,
        "showSafetyJudgement": True,
        "hapticBendPercentile": 50,
        "hapticFeedbackWindow": 600000,
        "showSafetyScoreModal": False,
        "exposureHapticEnabled": True,
        "exposureHapticRepeatMS": 10000,
        "hapticSingleBendWindow": 600,
        "hapticSagAngleThreshold": 65,
        "exposureHapticSuppressMS": 30000,
    }
    db_created_at = datetime.datetime.now()
    external_admin_user = factory.SubFactory(ExternalAdminUserFactory)

    class Meta:
        model = Setting
        sqlalchemy_session_persistence = "commit"


class JobFunctionFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    warehouse = factory.SubFactory(WarehouseFactory)
    name = factory.Faker("first_name")
    db_created_at = datetime.datetime.now()
    db_modified_at = datetime.datetime.now()
    max_package_mass = factory.fuzzy.FuzzyDecimal(3.0, 20.0, 2)
    color = "Null"
    avg_package_weight = 0
    description = factory.Faker("sentence")
    override_settings = 0
    lbd_indicence = 0
    lbd_indicence_rate = 0
    max_package_weight = 0
    min_package_weight = 0
    standard_score = 0
    settings = factory.SubFactory(SettingsFactory)

    class Meta:
        model = JobFunction
        sqlalchemy_session_persistence = "commit"


class IndustrialAthleteFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    client = factory.SubFactory(ClientFactory)
    warehouse = factory.SubFactory(WarehouseFactory)
    job_function = factory.SubFactory(JobFunctionFactory)
    shifts = factory.SubFactory(ShiftsFactory)
    gender = factory.fuzzy.FuzzyChoice(["f", "m"])
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    external_id = str(uuid.uuid4())
    hire_date = datetime.datetime.now()

    class Meta:
        model = IndustrialAthlete
        sqlalchemy_session_persistence = "commit"

    class Params:
        custom_client_id = None


class UserWarehouseAssociationFactory(factory.alchemy.SQLAlchemyModelFactory):
    external_admin_user = factory.SubFactory(ExternalAdminUserFactory)
    warehouse = factory.SubFactory(WarehouseFactory)

    class Meta:
        model = UserWarehouseAssociation
        sqlalchemy_session_persistence = "commit"


class UserRoleAssociationFactory(factory.alchemy.SQLAlchemyModelFactory):
    external_admin_user = factory.SubFactory(ExternalAdminUserFactory)
    role = random_str()

    class Meta:
        model = UserRoleAssociation
        sqlalchemy_session_persistence = "commit"


class UserClientAssociationFactory(factory.alchemy.SQLAlchemyModelFactory):
    external_admin_user = factory.SubFactory(ExternalAdminUserFactory)
    client = factory.SubFactory(ClientFactory)

    class Meta:
        model = UserClientAssociation
        sqlalchemy_session_persistence = "commit"


class AthleteUploadStatusFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    username = str(uuid.uuid4())
    processed = factory.fuzzy.FuzzyInteger(1, 100)
    total = 100
    client_id = ClientFactory.id
    connection_id = random_str()

    class Meta:
        model = AthleteUploadStatus
        sqlalchemy_session_persistence = "commit"


class ImportedIndustrialAthleteFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    athlete_upload_status = factory.SubFactory(AthleteUploadStatusFactory)
    group_id = factory.Sequence(lambda n: n)
    client_id = ClientFactory.id
    warehouse_id = WarehouseFactory.id
    shift_id = ShiftsFactory.id
    job_function_id = JobFunctionFactory.id
    gender = factory.fuzzy.FuzzyChoice(["f", "m"])
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    external_id = str(uuid.uuid4())
    weight = factory.fuzzy.FuzzyInteger(60, 100)
    height = factory.fuzzy.FuzzyInteger(150, 200)
    hire_date = datetime.datetime.now()
    termination_date = datetime.datetime.now()

    class Meta:
        model = ImportedIndustrialAthlete
        sqlalchemy_session_persistence = "commit"


class CasbinRuleFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    ptype = "p"
    v0 = factory.fuzzy.FuzzyChoice(["admin", "manager"])
    v1 = factory.fuzzy.FuzzyChoice(
        [
            "athletes",
            "clients",
            "shifts",
            "docks",
            "warehouses",
            "jobfunctions",
            "roles",
            "bulkupload",
        ]
    )
    v2 = factory.fuzzy.FuzzyChoice(["get", "post", "put", "delete"])

    class Meta:
        model = CasbinRule
        sqlalchemy_session_persistence = "commit"


class SensorsFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    serial_number = factory.fuzzy.FuzzyText(length=45)
    sensor_id = factory.fuzzy.FuzzyText(length=45)
    stiction_flagged = factory.fuzzy.FuzzyChoice(["0", "1"])
    decommissioned = factory.fuzzy.FuzzyChoice(["0", "1"])

    class Meta:
        model = Sensors
        sqlalchemy_session_persistence = "commit"


class GroupsFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    title = factory.fuzzy.FuzzyText(length=45)
    description = factory.fuzzy.FuzzyText(length=45)
    db_created_at = datetime.datetime.now()
    override_settings = factory.fuzzy.FuzzyChoice([True, False])
    industrial_athletes = factory.SubFactory(IndustrialAthleteFactory)

    class Meta:
        model = Groups
        sqlalchemy_session_persistence = "commit"
