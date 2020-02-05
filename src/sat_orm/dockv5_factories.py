'''
LICENSE:
    This file is subject to the terms and conditions defined in
    file 'LICENSE.txt', which is part of this source code package.
 
CONTRIBUTORS: 
            Vincent Turnier
            Norberto Fernandez

CLASSIFICATION: 
            Highly Sensitive

    **** Add Contributors name if you have contributed to this file ****
*********************************************************************************

DESCRIPTION:
            The dockv5_orm package is a presentation of the orms for the dockv5
            schema. As the table schema is deliccate and can affect other
            files when changes, the goal of the orm is to match with the
            schema at all times, meaning that we can now represent the 
            dockv5 schema as lines of code.
            
            +---------------+
            | Dockv5 Tables |
            +---------------+
            | config        |
            | dock_phase    |
            +---------------+

            **** Edit This File If tables are added or removed ****
'''

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
    while(count<6):
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
