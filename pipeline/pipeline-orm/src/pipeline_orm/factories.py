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
    
    class Meta:
        model = Client 
        sqlalchemy_session_persistence = 'commit'


class IndustrialAthleteFactory(factory.alchemy.SQLAlchemyModelFactory):

    gender = factory.fuzzy.FuzzyChoice(['f','m'])
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    external_id = str(uuid.uuid4())

    class Meta:
        model = IndustrialAthlete
        sqlalchemy_session_persistence = 'commit'




