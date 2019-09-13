import factory
import factory.fuzzy

import random
import string
import datetime


from config import Config, DockPhase

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

local_conntection_string = "mysql+pymysql://root:password@localhost/dockv5"
engine = create_engine(local_conntection_string)

Session = sessionmaker(bind=engine)
session = Session()

def generate_dock_id():
    hex_letters = ['A','B','C','D','E','F']
    count = 0
    dock_id = ''
    while(count<7):
        dock_id += random.choice(hex_letters)+random.choice(string.digits)
        count+=1
    return dock_id

class ConfigFactory(factory.alchemy.SQLAlchemyModelFactory):
    dock_id = generate_dock_id()
    client_id = 9999 #client id 9999 for all test client 
    warehouse_id = factory.fuzzy.FuzzyInteger(low=10000,high=11000,step=1)
    deployment_stage = factory.fuzzy.FuzzyChoice(['DEV','PROD'])
    
    @factory.post_generation
    def dock_phases(self, create, extracted, **kwargs):
        if extracted is None:
            extracted = 0

        make_dock_phase = getattr(DockPhaseFactory, 'create' if create else 'build')
        self.dock_phases = [make_dock_phase(config_id=self.id) for i in range(extracted)]

        if not create:
            self._prefetched_objects_cache = {'dock_phases':self.dock_phases}


    class Meta:
        model = Config
        sqlalchemy_session_persistence = 'commit'


class DockPhaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    config_id = factory.SubFactory(ConfigFactory)
    timestamp = factory.LazyFunction(datetime.datetime.now)
    phase = factory.fuzzy.FuzzyChoice(['PREP','INFIELD','DEMO','MAINTENANCE','UNUSED','RETIRED'])

    class Meta:
        model = DockPhase
        sqlalchemy_session_persistence = 'commit'

if __name__=='__main__':
    ConfigFactory._meta.sqlalchemy_session = session
    DockPhaseFactory._meta.sqlalchemy_session = session
    config = ConfigFactory.build(dock_phases=2)
    print(config)
    dock_phase = DockPhaseFactory.build()
    print(dock_phase)