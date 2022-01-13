import os

from copy import deepcopy

from sqlalchemy.sql.functions import GenericFunction
from sqlalchemy.types import DateTime

from sqlalchemy.exc import DBAPIError
from sqlalchemy_wrapper import SQLAlchemy


if RUNTIME_ENV == "LAMBDA":
    from config import Config
else:
    from pipeline.config import Config

db = SQLAlchemy(Config.DB_URL)
UTC_TIMEZONE = "UTC"


def commit_or_rollback(session):
    try:
        session.commit()
    except DBAPIError:
        session.rollback()
        raise


class convert_tz(GenericFunction):
    type = DateTime


from .config import Config
