'''
Author = Vincent Turnier
Created = September 16, 2019
Note:
    Make sure to checkout out database-models/wiki to learn more about testing
    link: https://github.com/strongarm-tech/database_models/wiki/Database-Testing

Description:
    The following will test
    1 - what happens when you insert into the config table
    2 - update the config table
    3 - query the config table
    4 - insert into the dock_phase table
    5 - query dock_phase table 
    6 - the relationship between the tables
'''
import pytest

from dockv5_orm.config import Config

def test_insert_into_config_table(session,config_factory):
    config_factory = config_factory
    before_insert = session.query(Config).count()
    config = Config(dock_id=config_factory.dock_id,
                    client_id = config_factory.client_id,
                    warehouse_id = config_factory.warehouse_id,
                    deployment_stage=config_factory.deployment_stage)
    session.add(config)
    session.commit()
    after_insert = session.query(Config).count()
    assert before_insert != after_insert


def test_get_config_table_with_dock_phase(session):
    config = session.query(Config).filter_by(dock_id='E423540B64BE').first()
    for dock_phase in config.dock_phases:
        assert dock_phase.dock_id == 'E423540B64BE'

def test_config_trigger_update_config_table(session):
    config = session.query(Config).filter_by(dock_id='E423540B64BE').first()
    dock_phase = config.dock_phases[0]
    dock_phase_count = len(config.dock_phases)
    dock_phase_deployment_stage = dock_phase.deployment_stage.lower()
    if dock_phase_deployment_stage == 'dev':
        new_dock_phase_deployment_stage = 'prod'
    else:
        new_dock_phase_deployment_stage = 'dev'
    update_config = session.query(Config).filter_by(dock_id='E423540B64BE').update({"deployment_stage":new_dock_phase_deployment_stage})
    session.commit()
    config = session.query(Config).filter_by(dock_id='E423540B64BE').first()
    dock_phase = config.dock_phases[0]
    new_dock_phase_count = len(config.dock_phases)
    assert dock_phase_count != new_dock_phase_count
    assert new_dock_phase_deployment_stage == dock_phase.deployment_stage.lower()








    

