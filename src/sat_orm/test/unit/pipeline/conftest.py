# Standard Library
import os
import random
import uuid

# Third Party Import
import pytest
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
import time
import copy
import uuid

# Local Application Import
from sat_orm.pipeline_factories import (
    ClientFactory,
    WarehouseFactory,
    ShiftsFactory,
    SettingsFactory,
    JobFunctionFactory,
    IndustrialAthleteFactory,
    ExternalAdminUserFactory,
    AthleteUploadStatusFactory,
    ImportedIndustrialAthleteFactory,
    CasbinRuleFactory,
    UserWarehouseAssociationFactory,
    SensorsFactory,
    GroupsFactory,
    UserRoleAssociationFactory,
)
from sat_orm.pipeline import (
    get_session,
    Client,
    Warehouse,
    Shifts,
    Setting,
    IndustrialAthlete,
    ExternalAdminUser,
    JobFunction,
    ImportedIndustrialAthlete,
    AthleteUploadStatus,
    CasbinRule,
    Sensors,
    Groups,
)
from sat_orm.test.test_database.test_database_setup import create_test_db
from sat_orm import constants

# import sat_orm.constants as constants
from sat_orm.constants import (
    LOGZIO_REQUIRED_KEYS,
    VALID_CLIENT_STATUSES,
    VALID_SHIFT_TIMEZONES,
    VALID_CLIENT_IA_NAME_FORMATS,
    RBAC_VALID_ROLES,
    RBAC_VALID_RESOURCES,
    RBAC_VALID_ACTIONS,
    VALID_CSV_STRING,
    INVALID_CSV_STRING_MISSING_HEADER,
)


os.environ["ENV_NAME"] = "test"


def pytest_configure(config):
    """Adds custom test makers"""
    config.addinivalue_line(
        "markers", "input_validation: mark test to run only database validations"
    )
    config.addinivalue_line(
        "markers",
        "relationships: mark tests to run only database foreign key relationships",
    )
    config.addinivalue_line(
        "markers", "test_inserts: mark tests to run only database insert actions"
    )
    config.addinivalue_line(
        "markers", "test_updates: mark tests to run only database update actions"
    )
    config.addinivalue_line(
        "markers", "test_delete: mark tests to run only database delete actions"
    )
    config.addinivalue_line(
        "markers", "orm_base: mark tests to run only sqlalchemy base module test"
    )
    config.addinivalue_line(
        "markers", "test_factories: mark tests to run only factories"
    )
    config.addinivalue_line(
        "markers", "test_return_type: mark tests to run only orm function return types"
    )
    config.addinivalue_line(
        "markers", "test_select : mark tests to run only to verify select queries"
    )


@pytest.fixture(scope="session")
def test_session():
    is_created, error = create_test_db("pipeline")
    if is_created:
        os.environ[
            "PIPELINE_CONNECTION_STRING"
        ] = "mysql+pymysql://root:password@127.0.01:3306/test_pipeline"
        """ Database Session created from db connection fixture"""
        with get_session() as session:
            ClientFactory._meta.sqlalchemy_session = session
            WarehouseFactory._meta.sqlalchemy_session = session
            ShiftsFactory._meta.sqlalchemy_session = session
            SettingsFactory._meta.sqlalchemy_session = session
            JobFunctionFactory._meta.sqlalchemy_session = session
            IndustrialAthleteFactory._meta.sqlalchemy_session = session
            ExternalAdminUserFactory._meta.sqlalchemy_session = session
            AthleteUploadStatusFactory._meta.sqlalchemy_session = session
            ImportedIndustrialAthleteFactory._meta.sqlalchemy_session = session
            CasbinRuleFactory._meta.sqlalchemy_session = session
            UserWarehouseAssociationFactory._meta.sqlalchemy_session = session
            UserRoleAssociationFactory._meta.sqlalchemy_session = session
            GroupsFactory._meta.sqlalchemy_session = session
            SensorsFactory._meta.sqlalchemy_session = session
            # Reset the factory id values to greater than the records to avoid duplicate id errors
            client = session.query(func.max(Client.id)).first()
            warehouse = session.query(func.max(Warehouse.id)).first()
            shift = session.query(func.max(Shifts.id)).first()
            setting = session.query(func.max(Setting.id)).first()
            job_function = session.query(func.max(JobFunction.id)).first()
            industrial_athlete = session.query(func.max(IndustrialAthlete.id)).first()
            external_admin_user = session.query(func.max(ExternalAdminUser.id)).first()
            athlete_upload_status = session.query(
                func.max(AthleteUploadStatus.id)
            ).first()
            imported_ia = session.query(func.max(ImportedIndustrialAthlete.id)).first()
            casbin_rule = session.query(func.max(CasbinRule.id)).first()
            group = session.query(func.max(Groups.id)).first()
            sensor = session.query(func.max(Sensors.id)).first()
            client_max_id = 1
            warehouse_max_id = 1
            shift_max_id = 1
            setting_max_id = 1
            job_function_max_id = 1
            industrial_athlete_max_id = 1
            external_admin_user_max_id = 1
            athlete_upload_status_max_id = 1
            imported_id_max_id = 1
            casbin_rule_max_id = 1
            group_max_id = 1
            sensor_max_id = 1
            if client[0] is not None:
                client_max_id = client[0] + 1
            if warehouse[0] is not None:
                warehouse_max_id = warehouse[0] + 1
            if shift[0] is not None:
                shift_max_id = shift[0] + 1
            if setting[0] is not None:
                setting_max_id = setting[0] + 1
            if job_function[0] is not None:
                job_function_max_id = job_function[0] + 1
            if industrial_athlete[0] is not None:
                industrial_athlete_max_id = industrial_athlete[0] + 1
            if external_admin_user[0] is not None:
                external_admin_user_max_id = external_admin_user[0] + 1
            if athlete_upload_status[0] is not None:
                athlete_upload_status_max_id = athlete_upload_status[0] + 1
            if imported_ia[0] is not None:
                imported_id_max_id = imported_ia[0] + 1
            if casbin_rule[0] is not None:
                casbin_rule_max_id = casbin_rule[0] + 1
            if group[0] is not None:
                group_max_id = group[0] + 1
            if sensor[0] is not None:
                sensor_max_id = sensor[0] + 1
            ClientFactory.reset_sequence(client_max_id)
            WarehouseFactory.reset_sequence(warehouse_max_id)
            ShiftsFactory.reset_sequence(shift_max_id)
            SettingsFactory.reset_sequence(setting_max_id)
            JobFunctionFactory.reset_sequence(job_function_max_id)
            IndustrialAthleteFactory.reset_sequence(industrial_athlete_max_id)
            ExternalAdminUserFactory.reset_sequence(external_admin_user_max_id)
            AthleteUploadStatusFactory.reset_sequence(athlete_upload_status_max_id)
            ImportedIndustrialAthleteFactory.reset_sequence(imported_id_max_id)
            CasbinRuleFactory.reset_sequence(casbin_rule_max_id)
            GroupsFactory.reset_sequence(group_max_id)
            SensorsFactory.reset_sequence(sensor_max_id)

            yield session
    else:
        RuntimeError(error)


# Random Database Objects
@pytest.fixture(scope="session", autouse=True)
def get_external_admin_user(test_session):
    new_client = ClientFactory()
    new_warehouse = WarehouseFactory(client=new_client)
    user = ExternalAdminUserFactory(client=new_client)
    UserRoleAssociationFactory(external_admin_user=user, role="superuser")

    UserWarehouseAssociationFactory(external_admin_user=user, warehouse=new_warehouse)
    for _ in range(random.randint(1, 4)):
        temp_warehouse = WarehouseFactory(client=new_client)
        UserWarehouseAssociationFactory(
            external_admin_user=user, warehouse=temp_warehouse
        )

    athlete_upload_status = AthleteUploadStatusFactory(
        username=user.username, client_id=user.client_id
    )

    for _ in range(4):
        new_jf = JobFunctionFactory(warehouse=new_warehouse)
        new_shift = ShiftsFactory(warehouse=new_warehouse)
        ia = IndustrialAthleteFactory(
            client=new_client,
            warehouse=new_warehouse,
            shifts=new_shift,
            job_function=new_jf,
            external_id=str(uuid.uuid4()),
        )
        ImportedIndustrialAthleteFactory(
            athlete_upload_status=athlete_upload_status,
            client_id=user.client_id,
            warehouse_id=new_warehouse.id,
            shift_id=new_shift.id,
            job_function_id=new_jf.id,
        )
        AthleteUploadStatusFactory(
            client_id=user.client_id, username=user.username, processed=100, total=100
        )
        GroupsFactory(industrial_athletes=[ia])
        SensorsFactory()
        SettingsFactory()
        test_session.commit()

    return user


@pytest.fixture(scope="function")
def get_industrial_athlete(get_external_admin_user, test_session):
    ia_list = (
        test_session.query(IndustrialAthlete)
        .filter_by(warehouse_id=get_external_admin_user.warehouses[0].warehouse_id)
        .filter_by(client_id=get_external_admin_user.client_id)
        .all()
    )
    random_ia = random.choice(ia_list)
    return random_ia


@pytest.fixture(scope="function")
def get_setting_type_athlete(get_industrial_athlete):
    """Builds settings from the Factories module"""
    ia = get_industrial_athlete
    return SettingsFactory.create(target_type="industrial_athlete", target_id=ia.id)


@pytest.fixture(scope="function")
def get_sensor_object(test_session):
    session = test_session
    """ Builds sensors from the Factories module"""
    return SensorsFactory.build()


@pytest.fixture(scope="function")
def get_sensor_from_db(test_session):
    """Builds sensors from the Factories module"""
    session = test_session
    return SensorsFactory.create()


@pytest.fixture(scope="function")
def get_warehouse_from_db(test_session):
    """Creates warehouse from the Factories module"""
    return WarehouseFactory.create()


@pytest.fixture(scope="function")
def get_group_from_db(test_session):
    """Creates group from the Factories module"""
    return GroupsFactory.create()


@pytest.fixture(scope="function")
def get_job_function_from_db(test_session):
    """Creates a JobFunction From the Factory"""
    return JobFunctionFactory.create()


@pytest.fixture(scope="function")
def get_random_shift(test_session, get_external_admin_user):
    shifts = (
        test_session.query(Shifts)
        .filter_by(warehouse_id=get_external_admin_user.warehouses[0].warehouse_id)
        .all()
    )
    return random.choice(shifts)


@pytest.fixture(scope="function")
def valid_int():
    return "0"


@pytest.fixture(scope="function")
def invalid_int():
    return "invalid int"


@pytest.fixture(scope="function")
def random_string():
    """
    Return a random string
    """
    return str(uuid.uuid4())


@pytest.fixture(scope="function")
def valid_string():
    return "09aA().-"


@pytest.fixture(scope="function")
def invalid_string():
    return "@/;#$%^&*()"


@pytest.fixture(scope="function")
def invalid_string_space_front():
    return " invalid"


@pytest.fixture(scope="function")
def valid_timezone():
    return random.choice(constants.VALID_SHIFT_TIMEZONES)


@pytest.fixture(scope="function")
def current_timestamp():
    millis = int(round(time.time() * 1000))
    return str(millis)


@pytest.fixture(scope="function")
def m_valid_sex():
    return "m"


@pytest.fixture(scope="function")
def valid_date():
    return "12/31/2020"


@pytest.fixture(scope="function")
def invalid_date():
    return "31/12/202"


@pytest.fixture(scope="function")
def valid_datetime():
    return "2020-12-01 10:49:00"


@pytest.fixture(scope="function")
def valid_first_name():
    return "John"


@pytest.fixture(scope="function")
def valid_last_name():
    return "Doe"


@pytest.fixture(scope="function")
def invalid_id():
    return 0


@pytest.fixture(scope="function")
def valid_email():
    return "abc@def.ghi"


@pytest.fixture(scope="function")
def valid_shift_fields():
    return random.choices(
        [
            "id",
            "name",
            "warehouse_id",
            "shift_start",
            "shift_end",
            "timezone",
            "group_administrator",
        ]
    )


@pytest.fixture(scope="function")
def valid_external_admin_user_fields():
    return [
        "id",
        "email",
        "username",
        "is_active",
        "warehouses",
        "client",
        "client_id",
    ]


@pytest.fixture(scope="function")
def create_external_admin_user_params(get_external_admin_user):
    temp_user = ExternalAdminUserFactory.build()
    return {
        "email": temp_user.email,
        "username": temp_user.username,
        "client_id": get_external_admin_user.client_id,
        "warehouse_id": get_external_admin_user.warehouses[0].warehouse_id,
    }


@pytest.fixture(scope="function")
def settings_factory(request):
    """Builds settings from the Factories module"""
    return SettingsFactory.create()


@pytest.fixture(scope="function")
def client_factory(request):
    """Builds clients from the Factories module"""
    return ClientFactory.create()


@pytest.fixture(scope="function")
def valid_ia_put_body(
    get_external_admin_user,
    valid_string,
    invalid_string_space_front,
    current_timestamp,
    m_valid_sex,
    valid_date,
    valid_first_name,
    valid_last_name,
    test_session,
):
    warehouse_id = get_external_admin_user.warehouses[0].warehouse_id
    ia_list = (
        test_session.query(IndustrialAthlete)
        .filter_by(warehouse_id=warehouse_id)
        .filter_by(client_id=get_external_admin_user.client_id)
        .all()
    )
    random_ia = random.choice(ia_list)

    job_function = random.choice(
        test_session.query(JobFunction).filter_by(warehouse_id=warehouse_id).all()
    )
    shift = random.choice(
        test_session.query(Shifts).filter_by(warehouse_id=warehouse_id).all()
    )

    return {
        "username": get_external_admin_user.username,
        "id": random_ia.id,
        "firstName": valid_first_name,
        "lastName": valid_last_name,
        "externalId": current_timestamp,
        "sex": m_valid_sex,
        "sexChangeDate": valid_date,
        "shiftId": shift.id,
        "jobFunctionId": job_function.id,
        "jobFunctionChangeDate": valid_date,
        "hireDate": valid_date,
        "clientId": shift.warehouse.client_id,
        "warehouseId": warehouse_id,
        "terminationDate": valid_date,
    }


@pytest.fixture(scope="function")
def invalid_athletes_put_body_invalid_first_name(
    valid_ia_put_body, invalid_string_space_front
):
    invalid_first_name = copy.deepcopy(valid_ia_put_body)
    invalid_first_name.pop("username")
    invalid_first_name["firstName"] = invalid_string_space_front
    return invalid_first_name


@pytest.fixture(scope="function")
def invalid_athletes_put_body_invalid_last_name(
    valid_ia_put_body, invalid_string_space_front
):
    invalid_last_name = copy.deepcopy(valid_ia_put_body)
    invalid_last_name.pop("username")
    invalid_last_name["lastName"] = invalid_string_space_front
    return invalid_last_name


@pytest.fixture(scope="function")
def valid_client_post_event(
    get_external_admin_user, random_string, valid_int, valid_date
):
    """
    Valid client post event
    """
    return {
        "username": get_external_admin_user.username,
        "name": random_string,
        "status": random.choice(VALID_CLIENT_STATUSES),
        "contracted_users": valid_int,
        "active_inactive_date": valid_date,
        "ia_name_format": random.choice(VALID_CLIENT_IA_NAME_FORMATS),
    }


@pytest.fixture(scope="function")
def invalid_client_post_event(
    get_external_admin_user, invalid_string_space_front, invalid_int
):
    """
    Invalid client post event
    """
    return {
        "id": get_external_admin_user.client_id,
        "username": get_external_admin_user.username,
        "name": invalid_string_space_front,
        "status": invalid_string_space_front,
        "contracted_users": invalid_int,
        "active_inactive_date": invalid_date,
        "firstname_format": invalid_string_space_front,
        "lastname_format": invalid_string_space_front,
    }


@pytest.fixture(scope="function")
def valid_client_put_event(
    get_external_admin_user, random_string, valid_int, valid_datetime
):
    """
    Valid client put event
    """
    return {
        "client_id": get_external_admin_user.client_id,
        "name": random_string,
        "status": random.choice(VALID_CLIENT_STATUSES),
        "contracted_users": valid_int,
        "active_inactive_date": valid_datetime,
        "ia_name_format": random.choice(VALID_CLIENT_IA_NAME_FORMATS),
    }


@pytest.fixture(scope="function")
def invalid_client_put_event(
    get_external_admin_user, invalid_string_space_front, invalid_int
):
    """
    Invalid client put event
    """
    return {
        "client_id": get_external_admin_user.client_id,
        "name": invalid_string_space_front,
        "status": invalid_string_space_front,
        "contracted_users": invalid_int,
        "active_inactive_date": invalid_date,
        "enableProcessing": invalid_int,
    }


@pytest.fixture(scope="function")
def valid_client_delete_event(client_factory):
    """
    Valid client delete event
    """
    return {
        "client_id": client_factory.id,
    }


@pytest.fixture(scope="function")
def invalid_client_delete_event(invalid_int):
    """
    Invalid client delete event
    """
    return {
        "client_id": invalid_int,
    }
