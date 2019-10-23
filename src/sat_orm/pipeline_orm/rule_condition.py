# Standard Library Imports

# Third Party Imports

# Local Application Imports

class RuleCondition(Base):
    __tablename__='rule_condition'

    # Columns
    id = Column(Integer,primary_key=True,autoincrement=True)
    path = Column(String(255),nullable=False)
    operator = Column(String(255),nullable=False)
    value = Column(String(255),nullable=False)
    rule_id = Column(Integer, nullable=False)
    deleted = Column(Boolean,nullable=False, default='0')
    db_created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'),nullable=False)
    db_updated_at = Column(DateTime,server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),nullable=False)

    # relationships

    @validates('path')
    def validate_path(self,key,path):
        if path is None:
            raise Exception('path cannot be Null')
        else:
            return path
    
    @validates('operator')
    def validate_operator(self,key,operator):
        if operator is None:
            raise Exception('operator cannot be Null')
        else:
            return operator
    
    @validates('value')
    def validate_value(self,key,value):
        if value is None:
            raise Exception('value cannot be Null')
        else:
            return value
    
    @validates('rule_id')
    def validate_rule_id(self,key,rule_id):
        if rule_id is None:
            raise Exception('rule_id cannot be Null')
        else:
            return rule_id
    
    @validates('deleted')
    def validate_deleted(self,key,deleted):
        if deleted is None:
            raise Exception('deleted cannot be Null')
        else:
            return deleted
    
    