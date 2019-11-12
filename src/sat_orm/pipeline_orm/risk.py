'''
LICENSE:
    This file is subject to the terms and conditions defined in
    file 'LICENSE.txt', which is part of this source code package.
 
CONTRIBUTORS: 
            Vincent Turnier

CLASSIFICATION: 
            Highly Sensitive

    **** Add Contributors name if you have contributed to this file ****
*********************************************************************************
'''

# Standard Library Imports

# Third Party Imports

# Local Application Imports

class Risk(Base):
    __tablename__='risk'

    # Columns
    id = Column(Integer,primary_key=True,autoincrement=True)
    processed_file_id = Column(Integer,default=None,nullable=True)
    start_time = Column(DateTime,default=None,nullable=True)
    end_time = Column(DateTime,default=None,nullable=True)
    avg_twist_velocity = Column(Integer,default=None,nullable=True)
    lift_rate = Column(Integer,default=None,nullable=True)
    max_flexion = Column(Integer,default=None,nullable=True)
    average_flexion = Column(Integer,default=None,nullable=True)
    max_lateral_velocity = Column(Float,default=None,nullable=True)
    max_moment = Column(Float,default=None,nullable=True)
    risk_score = Column(Float,default=None,nullable=True)
    db_create_at = Column(DateTime,server_default=text('CURRENT_TIMESTAMP'),nullable=False)
    db_modified_at = Column(DateTime,server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),nullable=False)
    