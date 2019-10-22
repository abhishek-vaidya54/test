# Third Party Imports
import pytest 

# Local Application Imports
from sat_orm.pipeline import Setting

@pytest.mark.input_validation
def test_settings_validate_target_type():
    ''' Checks to see if target type is not Null'''
    with pytest.raises(Exception) as exec_info:
        assert Setting(target_type=None)
    assert 'cannot be Null' in str(exec_info.value)


@pytest.mark.input_validation
def test_setting_validate_target_id():
    ''' Checks to see if target_id is not Null'''
    with pytest.raises(Exception) as exec_info:
        assert Setting(target_id=None)
    assert 'cannot be Null' in str(exec_info.value)

@pytest.mark.test_return_type
def test_setting_as_dict_return_type():
    ''' checks to see if as_dict returns a dictionary'''
    setting = Setting()
    assert isinstance(setting.as_dict(),dict)

@pytest.mark.test_return_type
def test_setting___repr___returns_str():
    ''' checks to see if __repr__ returns a string object'''
    setting = Setting()
    assert isinstance(setting.__repr__(),str)

