# Standard Library
import os
import random

# Third Party Import
import pytest
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

# Local Application Import
from sat_orm.pipeline_factories import *
from sat_orm.pipeline import *
from sat_orm.test.test_database.test_database_setup import create_test_pipeline
from sat_orm import constants

os.environ["ENV_NAME"] = "test"


def pytest_configure(config):
    """ Adds custom test makers"""
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


@pytest.fixture(scope="module")
def test_session():
    is_created, error = create_test_pipeline()
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
            sensors = session.query(func.max(Sensors.id)).first()
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
            sensors_max_id = 1
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
            if sensors[0] is not None:
                sensors_max_id = sensors[0] + 1
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
            SensorsFactory.reset_sequence(sensors_max_id)

            yield session
    else:
        RuntimeError(error)


# Random Database Objects
@pytest.fixture(scope="module")
def get_external_admin_user(test_session):
    client = ClientFactory()
    warehouse = WarehouseFactory(client=client)
    user = ExternalAdminUserFactory(
        role="superuser", client=client, warehouse=warehouse
    )
    athlete_upload_status = AthleteUploadStatusFactory(
        username=user.username, client_id=user.client_id
    )

    for i in range(4):
        new_jf = JobFunctionFactory(warehouse=warehouse)
        new_shift = ShiftsFactory(warehouse=warehouse)
        IndustrialAthleteFactory(
            client=client,
            warehouse=warehouse,
            shifts=new_shift,
            job_function=new_jf,
        )
        ImportedIndustrialAthleteFactory(
            athlete_upload_status=athlete_upload_status,
            client_id=user.client_id,
            warehouse_id=user.warehouse_id,
            shift_id=new_shift.id,
            job_function_id=new_jf.id,
        )
        AthleteUploadStatusFactory(
            client_id=user.client_id, username=user.username, processed=100, total=100
        )

    return user

@pytest.fixture(scope="function")
def get_industrial_athlete(get_external_admin_user, test_session):
    ia_list = (
        test_session.query(IndustrialAthlete)
        .filter_by(warehouse_id=get_external_admin_user.warehouse_id)
        .filter_by(client_id=get_external_admin_user.client_id)
        .all()
    )
    random_ia = random.choice(ia_list)
    return random_ia


@pytest.fixture(scope="function")
def get_setting_type_athlete(get_industrial_athlete):
    """ Builds settings from the Factories module"""
    ia = get_industrial_athlete
    return SettingsFactory.create(
        target_type = "industrial_athlete",
        target_id = ia.id)

@pytest.fixture(scope="function")
def get_sensor_object(test_session):
    session = test_session
    """ Builds sensors from the Factories module"""
    return SensorsFactory.build()

@pytest.fixture(scope="function")
def get_sensor_from_db(test_session):
    """ Builds sensors from the Factories module"""
    session = test_session
    return SensorsFactory.create()

@pytest.fixture(scope="function")
def create_external_admin_user_params(get_external_admin_user):
    temp_user = ExternalAdminUserFactory.build()
    return {
        "email": temp_user.email,
        "username": temp_user.username,
        "client_id": get_external_admin_user.client_id,
        "warehouse_id": get_external_admin_user.warehouse_id,
    }

@pytest.fixture(scope="function")
def invalid_int():
    return "zero"

@pytest.fixture(scope="function")
def get_warehouse_from_db(test_session):
    """ Creates warehouse from the Factories module"""
    return WarehouseFactory.create()

@pytest.fixture(scope="function")
def get_random_shift(test_session, get_external_admin_user):
    shifts = (
        test_session.query(Shifts)
        .filter_by(warehouse_id=get_external_admin_user.warehouse_id)
        .all()
    )
    return random.choice(shifts)


@pytest.fixture(scope="function")
def invalid_int():
    return "invalid int"


@pytest.fixture(scope="function")
def invalid_string():
    return "@/;#$%^&*()"


@pytest.fixture(scope="function")
def valid_string():
    return "abcd-ABCD"


@pytest.fixture(scope="function")
def valid_timezone():
    return random.choice(constants.VALID_SHIFT_TIMEZONES)


@pytest.fixture(scope="function")
def valid_datetime():
    return "2018-06-19 14:51:35"


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
    return random.choices(
        [
            "id",
            "username",
            "email",
            "client_id",
            "warehouse_id",
            "role",
            "is_active",
        ]
    )


# @pytest.fixture(scope="session")
# def env():
#     """ Grab environment variables"""
#     variables = {}
#     variables["CONNECTION"] = os.environ.get("PIPELINE_CONNECTION_STRING", 0)
#     if variables["CONNECTION"]:
#         return variables["CONNECTION"]
#     else:
#         raise Exception(
#             'Please make sure Environment variables are set: export CONNECTION_STRING="db://username:password@host/database"'
#         )


# @pytest.fixture(scope="module")
# def engine(env):
#     """ Database engine created using the environment variable fixture"""
#     engine = create_engine(env)
#     return engine


# @pytest.fixture(scope="module")
# def session(engine):
#     """ Database Session created from db connection fixture"""
#     connection = engine.connect()
#     transaction = connection.begin()
#     Session = sessionmaker(bind=connection)
#     session = Session()
#     ClientFactory._meta.sqlalchemy_session = session
#     WarehouseFactory._meta.sqlalchemy_session = session
#     ShiftsFactory._meta.sqlalchemy_session = session
#     JobFunctionFactory._meta.sqlalchemy_session = session
#     IndustrialAthleteFactory._meta.sqlalchemy_session = session
#     yield session
#     session.close()
#     transaction.rollback()
#     connection.close()


# @pytest.fixture(scope="function")
# def industrial_athlete_factory():
#     """ Builds an IndustrialAthlete From the Factory"""
#     return IndustrialAthleteFactory.build()


# @pytest.fixture(scope="function")
# def job_function_factory():
#     """ Builds a JobFunction From the Factory"""
#     return JobFunctionFactory.build()


# @pytest.fixture(scope="function")
# def shift_factory():
#     """ Builds a Shift From the Factory"""
#     return ShiftsFactory.build()


# @pytest.fixture(scope="function")
# def warehouse_factory():
#     """ Builds a Warehouse From the Factory"""
#     return WarehouseFactory.build()


# @pytest.fixture(scope="function")
# def client_factory(request):
#     """ Builds clients from the Factories module"""
#     return ClientFactory.build()
