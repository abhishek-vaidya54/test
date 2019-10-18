from sat_orm.dockv5_orm.dockv5_base import Base, session, connection

from sat_orm.dockv5_orm.config import Config 
from sat_orm.dockv5_orm.dock_phase import DockPhase 

if __name__=='__main__':
    config = Config()
    config.insert_or_update()