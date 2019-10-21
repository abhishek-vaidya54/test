from sat_orm.dockv5_orm.dockv5_base import Base, session, connection

from sat_orm.dockv5_orm.config import Config 
from sat_orm.dockv5_orm.dock_phase import DockPhase 

if __name__=='__main__':
    config = Config()
    dock_phase = DockPhase()
    data = {
    "dock_id": "A4R3W4D5T6G7W9",
    "dock_imei": "12345E12345",
    "client_id": 716,
    "warehouse_id": 12345,
    "deployment_stage": "prod",
    "barcode_regex":"12345"
    }
    data1 = {
        "dock_id":data['dock_id'],
        "phase":"DEPLOYED"
    }
    config.insert_or_update(session,Config,data)
    dock_phase.update_phase(session=session,data=data1)
    session.commit()