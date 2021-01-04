# Third Party Imports
import pytest 

# Local Application Imports
from sat_orm.pipeline import Sensors

@pytest.mark.input_validation
def test_seensors_validate_serial_number():
    ''' Checks to see if serial number is not Null'''
    with pytest.raises(Exception) as exec_info:
        assert Sensors(serial_number=None)
    assert 'serial_number cannot be NULL' in str(exec_info.value)


@pytest.mark.input_validation
def test_sensors_validate_sensor_id():
    ''' Checks to see if sensor_id is not Null'''
    with pytest.raises(Exception) as exec_info:
        assert Sensors(target_id=None)

@pytest.mark.test_return_type
def test_sensors_as_dict_return_type():
    ''' checks to see if as_dict returns a dictionary'''
    sensor = Sensors()
    assert isinstance(sensor.as_dict(),dict)

@pytest.mark.test_return_type
def test_sensors___repr___returns_str():
    ''' checks to see if __repr__ returns a string object'''
    sensor = Sensors()
    assert isinstance(sensor.__repr__(),str)

def test_create(test_session, get_sensor_object):
    ''' checks to see if method creates a sensor object'''
    sensor_obj = get_sensor_object
    sensor = Sensors()
    res = sensor.create(
        test_session,
        sensor_obj.serial_number,
        sensor_obj.sensor_id
        )
    assert res.serial_number == sensor_obj.serial_number
    assert res.sensor_id == sensor_obj.sensor_id
    assert test_session.query(Sensors).filter_by(id=res.id)

def test_get_by_id(test_session, get_sensor_from_db):
    ''' checks to see if method return correct sensor object'''
    sensor = Sensors()
    res = sensor.get_by_id(test_session, get_sensor_from_db.id)
    assert res.id == get_sensor_from_db.id

def test_get_by_sensor_id(test_session, get_sensor_from_db):
    ''' checks to see if method return correct sensor object'''
    sensor_obj = get_sensor_from_db
    sensor = Sensors()
    res = sensor.get_by_sensor_id(test_session, sensor_obj.sensor_id)
    assert res.sensor_id == sensor_obj.sensor_id
    assert res.id == sensor_obj.id

def test_update_by_id(test_session, get_sensor_from_db, get_sensor_object):
    ''' checks to see if method updates sensor object correctly'''
    old_sensor = get_sensor_from_db
    new_sensor = get_sensor_object
    sensor = Sensors()
    res = sensor.update_by_id(
        test_session, 
        old_sensor.id,
        sensor_id = new_sensor.sensor_id,
        serial_number = old_sensor.serial_number,
        stiction_flagged = old_sensor.stiction_flagged,
        decommissioned = old_sensor.decommissioned
        )
    assert res.sensor_id == new_sensor.sensor_id
    assert res.serial_number == old_sensor.serial_number
    assert res.stiction_flagged == old_sensor.stiction_flagged
    assert res.decommissioned == old_sensor.decommissioned

def test_delete_by_sensor_id(test_session, get_sensor_from_db):
    ''' checks to see if method deletes sensors object correctly by sensor_id'''
    del_sensor = get_sensor_from_db
    sensor = Sensors()
    res = sensor.delete_by_sensor_id(test_session, del_sensor.sensor_id)
    myMan = test_session.query(Sensors).filter_by(id=del_sensor.id).first()
    assert not test_session.query(Sensors).filter_by(id=del_sensor.id).first()


def test_delete_by_id(test_session, get_sensor_from_db):
    ''' checks to see if method deletes sensors object correctly by id'''
    del_sensor = get_sensor_from_db
    sensor = Sensors()
    res = sensor.delete_by_id(test_session, del_sensor.id)
    assert not test_session.query(Sensors).filter_by(id=del_sensor.id).first()


