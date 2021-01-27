
from __future__ import with_statement

import os
import json

from alembic import context
from sqlalchemy import engine_from_config, pool, create_engine
from logging.config import fileConfig
from os.path import expanduser

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

VAULT_TOKEN = os.environ.get('VAULT_TOKEN', '')

# TODO: fix verify SSL error (and remove verify=False flag)
def get_vault_config(configName):
  config = None
  return config

def get_url():
    # if running in GitHub Action CI/CD
    if os.environ.get('CI'):
        # grab the database uri input by the user
        uri_interim = os.environ.get('INPUT_DATABASE_URI')
    else:
        local_db = os.environ.get('LOCAL_DOCK_DB_URI')
        dev_db = os.environ.get('DEV_DOCK_DB_URI')
        staging_db = os.environ.get('STAGING_DOCK_DB_URI')
        prod_db = os.environ.get('PROD_DOCK_DB_URI')
        uri_interim = local_db
    print("database URI:", uri_interim)
    return uri_interim

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(get_url())

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()