from sat_orm.dockv5_orm.dockv5_base import Base, session, connection

from sat_orm.dockv5_orm.config import Config 
from sat_orm.dockv5_orm.dock_phase import DockPhase 

if __name__=='__main__':
    config = Config()
    data = {
  "dock_id": "L4R3W4D5T6G7W9",
  "dock_imei": "12345E12345",
  "client_id": 712,
  "warehouse_id": 12345,
  "deployment_stage": "prod",
  "phase": "DEPLOYED",
  "barcode_regex":"12345"
}
    config.insert_or_update(session,data)