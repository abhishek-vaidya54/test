# Standard Library Imports

# Third Party Imports
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import validates

# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base

class MessageSurvey(Base):
    __tablename__='messages_surveys'

    # Columns
    id = Column(Integer, primary_key=True,autoincrement=True)
    engagement = Column(String(30),nullable=False)
    days_worn = Column(Integer,nullable=False)
    modal_type = Column(String(50),nullable=False)
    content = Column(JSON,nullable=True)

    # relatoionships

    @validates('engagement')
    def validate_engagement(self,key,engagement):
        if engagement is None:
            raise Exception('engagement cannot be Null')
        else:
            return engagement
    
    @validates('days_worn')
    def validate_days_worn(self,key,days_worn):
        if days_worn is None:
            raise Exception('days_worn cannot be Null')
        else:
            return days_worn
    
    @validates('modal_type')
    def validate_modal_type(self,key,modal_type):
        if modal_type is None:
            raise Exception('modal_type cannot be Null')
        else:
            return modal_type
    
