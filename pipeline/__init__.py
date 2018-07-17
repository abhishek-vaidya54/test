import os

from copy import deepcopy

from sqlalchemy.sql.functions import GenericFunction
from sqlalchemy.types import DateTime

from sqlalchemy.exc import DBAPIError
from sqlalchemy_wrapper import SQLAlchemy

DEPLOYMENT_STAGE = os.environ.get('DEPLOYMENT_STAGE','')

from config_DEV import Config as ConfigDev
from config_PROD import Config as ConfigProd

Config = None

if DEPLOYMENT_STAGE == 'PROD':
  Config = ConfigProd
else:
  Config = ConfigDev


db = SQLAlchemy(Config.DB_URL)
UTC_TIMEZONE = 'UTC'

def commit_or_rollback(session):
    try:
        session.commit()
    except DBAPIError:
        session.rollback()
        raise

class convert_tz(GenericFunction):
    type = DateTime


from .client import (
    Client
)
from .industrial_athlete import IndustrialAthlete, Tag, Group, groups
from .warehouse import Warehouse
from .processed_file import ProcessedFile
from .risk import Risk
from .shifts import Shifts
from .job_function import JobFunction
from .compliance_tracker import EmailSchedule
from .activity import Activity