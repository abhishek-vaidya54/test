'''
Contributor: Vincent Turnier
Date Edited: September 18th, 2019
Note:

Description:

'''
# Standard Library
import datetime

# Third Party Import
import factory
import factory.fuzzy
import uuid


# Local Application Import
from pipeline_orm.pipeline import *

class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    
    id = 99
    name = 'Test Client'
    db_created_at = datetime.datetime.now()
    db_modified_at = datetime.datetime.now()

    class Meta:
        model = Client 
        sqlalchemy_session_persistence = 'commit'

class WarehouseFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Warehouse 
        sqlalchemy_session_persistence = 'commit'

class ShiftsFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Shifts 
        sqlalchemy_session_persistence = 'commit'

class JobFunctionFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = JobFunction 
        sqlalchemy_session_persistence = 'commit'


class IndustrialAthleteFactory(factory.alchemy.SQLAlchemyModelFactory):

    client_id = 99
    warehouse_id = 999
    shift_id = 56
    job_function_id = 133
    gender = factory.fuzzy.FuzzyChoice(['f','m'])
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    external_id = str(uuid.uuid4())

    class Meta:
        model = IndustrialAthlete
        sqlalchemy_session_persistence = 'commit'




