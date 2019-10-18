import factory
import factory.fuzzy
import os
import random
import string
import datetime


from sat_orm.dockv5 import Config, DockPhase




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
    client_id = 9999
    warehouse_id = factory.fuzzy.FuzzyInteger(low=10000,high=11000,step=1)
    deployment_stage = factory.fuzzy.FuzzyChoice(['dev','prod'])
    
    @factory.post_generation
    def dock_phases(self, create, extracted, **kwargs):
        if extracted is None:
            extracted = 0

        make_dock_phase = getattr(DockPhaseFactory, 'create' if create else 'build')
        self.dock_phases = [make_dock_phase(dock_id=self.dock_id) for i in range(extracted)]

        if not create:
            self._prefetched_objects_cache = {'dock_phases':self.dock_phases}


    class Meta:
        model = Config
        sqlalchemy_session_persistence = 'commit'


class DockPhaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    dock_id = factory.SubFactory(ConfigFactory)
    timestamp = factory.LazyFunction(datetime.datetime.now)
    phase = factory.fuzzy.FuzzyChoice(['DEPLOYED','NOT DEPLOYED','MAINTENANCE'])
    
    class Meta:
        model = DockPhase
        sqlalchemy_session_persistence = 'commit'
