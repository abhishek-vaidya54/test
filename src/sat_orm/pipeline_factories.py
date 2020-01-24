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
from sat_orm.pipeline import Client, IndustrialAthlete, JobFunction, Warehouse, Shifts

class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    ''' Client Factory: creates a fake client with its relationships'''
    id = factory.Sequence(lambda n : n+1)
    name = factory.Sequence(lambda n : 'Test Client {0}'.format(n+1))
    prefix = factory.Sequence(lambda n : n+1)
    # guid = str(SmallUUID())
    # dynamic_shift = factory.Sequence(lambda n : n%2)
    db_created_at = datetime.datetime.now()
    db_modified_at = datetime.datetime.now()
    enable_processing = True

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
    ''' Warehouse Factory: creates a fake warehouse with its relationships if the relationships are not None'''
    id = factory.Sequence(lambda n: n+1)
    client_id = factory.SubFactory(ClientFactory)
    name = factory.Faker('first_name')
    location = factory.Faker('address')
    db_created_at = datetime.datetime.now()
    db_modified_at = datetime.datetime.now()
    prefered_timezone = 'US/Eastern'
    display_names = factory.Sequence(lambda n : n%2)
    utc_op_day_start = '00:00:00'
    week_start = factory.fuzzy.FuzzyChoice(['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'])
    show_engagement = factory.Sequence(lambda n : n%2)
    update_engagement = factory.Sequence(lambda n : n%2)
    hide_judgement = factory.Sequence(lambda n : n%2)

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
    
    @factory.post_generation
    def industrial_athlete(self,create,extracted, **kwargs):
        if extracted is None:
            extracted = 25
        
        make_industrial_athlete = getattr(IndustrialAthleteFactory,'create' if create else 'build')
        self.industrial_athletes = [make_industrial_athlete(client_id=self.client_id,
                                                            warehouse_id=self.id,
                                                            shift_id=self.shifts[0].id,
                                                            job_function_id=self.job_functions[0].id) for i in range(extracted)]
        

    class Meta:
        model = Warehouse 
        sqlalchemy_session_persistence = 'commit'

class ShiftsFactory(factory.alchemy.SQLAlchemyModelFactory):
    ''' Shift Factory: creates a fake shift as well as any of its relationships'''
    id = factory.Sequence(lambda n: n+1)
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

    id = factory.Sequence(lambda n : n+1)
    warehouse_id = factory.SubFactory(WarehouseFactory)
    name = factory.Faker('first_name')
    db_created_at = datetime.datetime.now()
    db_modified_at = datetime.datetime.now()
    max_package_mass = factory.fuzzy.FuzzyDecimal(3.0,20.0,2) 
    color = 'Null'
    avg_package_weight = 0
    description = factory.Faker('sentence')   
    group_administrator = factory.Faker('email')
    lbd_indicence = 0
    lbd_indicence_rate = 0
    max_package_weight = 0
    min_package_weight = 0
    standard_score = 0

    class Meta:
        model = JobFunction 
        sqlalchemy_session_persistence = 'commit'


class IndustrialAthleteFactory(factory.alchemy.SQLAlchemyModelFactory):

    id = factory.Sequence(lambda n: n+1)
    client_id = factory.SubFactory(ClientFactory)
    warehouse_id = factory.SubFactory(WarehouseFactory)
    job_function_id = factory.SubFactory(JobFunctionFactory)
    shift_id = factory.SubFactory(ShiftsFactory)
    gender = factory.fuzzy.FuzzyChoice(['f','m'])
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    external_id = str(uuid.uuid4())

    class Meta:
        model = IndustrialAthlete
        sqlalchemy_session_persistence = 'commit'
