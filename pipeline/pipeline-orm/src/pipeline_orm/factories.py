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
from smalluuid import SmallUUID

# Local Application Import
from pipeline_orm.pipeline import *

class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    ''' Client Factory: creates a fake client with its relationships'''
    id = 99
    name = 'Test Client'
    prefix = factory.fuzzy.FuzzyInteger(0,100,step=1)
    guid = str(SmallUUID())
    dynamic_shift = factory.fuzzy.FuzzyChoice([1,0])
    db_created_at = datetime.datetime.now()
    db_modified_at = datetime.datetime.now()

    @factory.post_generation
    def warehouse(self,create,extracted, **kwargs):
        if extracted is None:
            extracted = 3
        
        make_warehouses = getattr(WarehouseFactory,'create' if create else 'build')
        self.warehouses = [make_warehouses(client_id=self.id) for i in range(extracted)]

        if not create:
            self._prefetched_objects_cache = {'warehouses':self.warehouses}

    class Meta:
        model = Client 
        sqlalchemy_session_persistence = 'commit'

class WarehouseFactory(factory.alchemy.SQLAlchemyModelFactory):
    ''' Warehouse Factory: creates a fake warehouse with its relationships if the relationships are not None
        ie: Warehouse.build(job_functions=4,shifts=4)'''
    # TODO: figure out how ids will be created
    id = factory.Sequence(lambda n: n)
    client_id = factory.SubFactory(ClientFactory)
    name = factory.Faker('first_name')
    location = factory.Faker('address')
    db_created_at = datetime.datetime.now()
    db_modified_at = datetime.datetime.now()
    prefered_timezone = 'US/Eastern'
    display_names = factory.fuzzy.FuzzyChoice([1,0])
    utc_op_day_start = '00:00:00'
    week_start = factory.fuzzy.FuzzyChoice(['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'])
    show_engagement = factory.fuzzy.FuzzyChoice([1,0])
    update_engagement = factory.fuzzy.FuzzyChoice([1,0])
    hide_judgement = factory.fuzzy.FuzzyChoice([1,0])

    @factory.post_generation
    def job_functions(self,create,extracted,**kwargs):
        if extracted is None:
            extracted = 1
        
        make_job_functions = getattr(JobFunctionFactory,'create' if create else 'build')
        self.job_functions = [make_job_functions(warehouse_id=self.id) for i in range(extracted)]

        if not create:
            self._prefetched_objects_cache = {'job_functions':self.job_functions}
    
    @factory.post_generation
    def shifts(self,create,extracted, **kwargs):
        if extracted is None:
            extracted = 2

        make_shifts = getattr(ShiftsFactory,'create' if create else 'build')
        self.shifts = [make_shifts(warehouse_id=self.id) for i in range(extracted)]

        if not create:
            self._prefetched_objects_cache = {'shifts':self.shifts}

    class Meta:
        model = Warehouse 
        sqlalchemy_session_persistence = 'commit'

class ShiftsFactory(factory.alchemy.SQLAlchemyModelFactory):

    id = factory.Sequence(lambda n: n)
    warehouse_id = factory.SubFactory(WarehouseFactory)
    name = factory.fuzzy.FuzzyChoice(['Shift 1','Shift 2','Shift 3'])
    shift_start = datetime.time(hour=7,minute=0,second=0)
    shift_end = datetime.time(hour=15,minute=0,second=0)
    db_created_at = datetime.datetime.now()
    db_modified_at = datetime.datetime.now()
    color = None
    description = factory.Faker('sentence')
    group_administrator = factory.Faker('email')

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





if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    import os 

    engine = create_engine(os.environ.get('CONNECTION_STRING'))
    Session = sessionmaker(bind=engine)
    session = Session()
    ClientFactory._meta.sqlalchemy_session = session
    client_factory = ClientFactory.build()
    print(client_factory)
    for warehouse in client_factory.warehouses:
        print(warehouse)