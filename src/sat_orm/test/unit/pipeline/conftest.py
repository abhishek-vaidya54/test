# Standard Library
import os

# Third Party Import
import pytest
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

# Local Application Import
from sat_orm.pipeline_factories import *
from sat_orm.pipeline import *
from sat_orm.test.test_database.test_database_setup import create_test_pipeline
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

            yield session
    else:
        RuntimeError(error)


# Random Database Objects
@pytest.fixture(scope="session")
def get_external_admin_user(test_session):
    user = ExternalAdminUserFactory(role="superuser")
    athlete_upload_status = AthleteUploadStatusFactory(
        username=user.username, client_id=user.client_id
    )

    for i in range(4):
        new_jf = JobFunctionFactory(warehouse=user.warehouse)
        new_shift = ShiftsFactory(warehouse=user.warehouse)
        new_ia = IndustrialAthleteFactory(
            client=user.client,
            warehouse=user.warehouse,
            shifts=new_shift,
            job_function=new_jf,
        )
        new_imported_ia = ImportedIndustrialAthleteFactory(
            athlete_upload_status=athlete_upload_status,
            client_id=user.client_id,
            warehouse_id=user.warehouse_id,
            shift_id=new_shift.id,
            job_function_id=new_jf.id,
        )
        new_upload_status = AthleteUploadStatusFactory(
            client_id=user.client_id, username=user.username, processed=100, total=100
        )

    return user


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


@pytest.fixture(scope="function")
def client_factory(request):
    """ Builds clients from the Factories module"""
    return ClientFactory.create()


@pytest.fixture(scope="function")
def invalid_string_space_front():
    return " invalid"

@pytest.fixture(scope="function")
def random_string():
    """
    Return a random string
    """
    return str(uuid.uuid4())

@pytest.fixture(scope="function")
def valid_int():
    return "0"

@pytest.fixture(scope="function")
def invalid_int():
    return "zero"

@pytest.fixture(scope="function")
def valid_date():
    return "12/31/2020"

@pytest.fixture(scope="function")
def valid_datetime():
    return "2020-12-01 10:49:00"

@pytest.fixture(scope="function")
def invalid_date():
    return "31/12/202"

@pytest.fixture(scope="function")
def valid_string():
    return "09aA().-"


@pytest.fixture(scope="function")
def valid_first_name():
    return "John"


@pytest.fixture(scope="function")
def valid_last_name():
    return "Doe"


@pytest.fixture(scope="function")
def invalid_string_space_front():
    return " invalid"

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
            "enableProcessing": invalid_int

        }

@pytest.fixture(scope="function")
def valid_client_delete_event(
    client_factory
):
    """
    Valid client delete event
    """
    return {
            "client_id": client_factory.id,
        }

@pytest.fixture(scope="function")
def invalid_client_delete_event(
    invalid_int
):
    """
    Invalid client delete event
    """
    return {
            "client_id": invalid_int,

        }