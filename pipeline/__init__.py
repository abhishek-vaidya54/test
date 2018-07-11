import os

from copy import deepcopy

from sqlalchemy.sql.functions import GenericFunction
from sqlalchemy.types import DateTime

from sqlalchemy.exc import DBAPIError
from sqlalchemy_wrapper import SQLAlchemy

from influxdb import InfluxDBClient

RUNTIME_ENV = os.environ.get('RUNTIME_ENV','')

if RUNTIME_ENV == 'LAMBDA':
    from config import Config
else:
    from pipeline.config import Config
    from pipeline.server.constant_data import COLOR_CHOICES


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


def get_color_choices(model, warehouse_id, selected_color=None):
    used_colors = db.session.query(model.color.label('color')).filter(
        model.warehouse_id == warehouse_id,
    ).filter(model.color != None).distinct()
    used_colors = [used_color.color for used_color in used_colors]
    colors = deepcopy(COLOR_CHOICES)
    for index, color in enumerate(colors):
        if color[0] in used_colors and selected_color != color[0]:
            del colors[index]
    return colors


def get_influx_client():
    influxdb_client = InfluxDBClient(
    host=Config.INFLUXDB_HOST,
    port=Config.INFLUXDB_PORT,
    username=Config.INFLUXDB_USERNAME,
    password=Config.INFLUXDB_PASSWORD,
    database=Config.INFLUXDB_DATABASE,
    ssl=Config.INFLUXDB_SSL,
    verify_ssl=True,
    timeout=1
    )


    return influxdb_client
