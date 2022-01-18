# Standard Library Imports

# Third Party Imports
import pytest

# Local Application Imports
from sat_orm.pipeline import *


@pytest.mark.test_factories
def test_industrial_athlete_factory_relationships(industrial_athlete_factory):
    ia_factory = industrial_athlete_factory
    assert isinstance(ia_factory.client_id, Client)
    assert isinstance(ia_factory.warehouse_id, Warehouse)
    assert isinstance(ia_factory.job_function_id, JobFunction)
    assert isinstance(ia_factory.shift_id, Shifts)


@pytest.mark.test_factories
def test_job_function_factory_warehouse_factory_relationship(job_function_factory):
    jf_factory = job_function_factory
    assert isinstance(jf_factory.warehouse_id, Warehouse)


@pytest.mark.test_factories
def test_shifts_factory_warehouse_factory_relationship(shift_factory):
    s_factory = shift_factory
    assert isinstance(s_factory.warehouse_id, Warehouse)


@pytest.mark.test_factories
def test_warehouse_factory_client_factory_relationship(warehouse_factory):
    wh_factory = warehouse_factory
    assert isinstance(wh_factory.client_id, Client)


@pytest.mark.test_factories
def test_warehouse_factory_job_functions(warehouse_factory):
    wh_factory = warehouse_factory
    job_functions = wh_factory.job_functions
    assert len(job_functions) == 1


@pytest.mark.test_factories
def test_warehouse_factory_shifts(warehouse_factory):
    wh_factory = warehouse_factory
    shifts = wh_factory.shifts
    assert len(shifts) == 2


@pytest.mark.test_factories
def test_warehouse_factory_industrial_athlete(warehouse_factory):
    wh_factory = warehouse_factory
    industrial_athletes = wh_factory.industrial_athletes
    assert len(industrial_athletes) == 25


@pytest.mark.test_factories
def test_client_factory_warehouse(get_external_admin_user):
    client = get_external_admin_user.client
    warehouses = client.warehouses
    assert warehouses
