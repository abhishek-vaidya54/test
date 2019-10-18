from sat_orm.dockv5_orm.dockv5_base import Base, session, connection

from sat_orm.dockv5_orm.config import Config 
from sat_orm.dockv5_orm.dock_phase import DockPhase 

if __name__=='__main__':
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    engine = create_engine('mysql+pymysql://root:password@localhost/dockv5')
    Session = sessionmaker(bind=engine)
    session = Session()
    config = Config()
    config.insert_or_update()