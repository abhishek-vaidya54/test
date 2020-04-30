import datetime

from sqlalchemy import ForeignKey, Column, String, Integer, DateTime , desc
from sqlalchemy.orm import relationship, validates

from sat_orm.pipeline_orm.pipeline_base import Base

class Sensors(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    serial_number = Column(String(45), nullable=False)
    sensor_id = Column(String(45), nullable=True)
    stiction_flagged = Column(
        String(45),
        default='0',
        nullable=False
    )
    decommissioned = Column(String(45),
        default='0',
        nullable=False
    )
    
    db_created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    db_modified_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )

    @validates('serial_number')
    def validate_serial_number(self, key, serial_number):
        if serial_number == None:
            raise Exception('serial_number cannot be NULL')
        if len(serial_number) > 45:
            raise Exception('serial_number cannot be more than 45 characters long')
        return serial_number.strip()

    @validates('sensor_id')
    def validate_sensor_id(self, key, sensor_id):
        if sensor_id == None:
            return None
        return sensor_id.strip()

    @validates('stiction_flagged')
    def validate_flagged(self, key, stiction_flagged):
        if stiction_flagged == None:
            raise Exception('stiction_flagged cannot be NULL')
        if stiction_flagged != '0' and stiction_flagged != '1':
            raise Exception('stiction_flagged can only be either 0 or 1')
        return stiction_flagged.strip()

    @validates('decommissioned')
    def validate_decommissioned(self, key, decommissioned):
        if decommissioned == None:
            raise Exception('decommissioned cannot be NULL')
        if decommissioned != '0' and decommissioned != '1':
            raise Exception('decommissioned can only be either 0 or 1')
        return decommissioned.strip()

    def as_dict(self):
        return {
            "id": self.id,
            "serialNumber": self.serial_number,
            "sensorId": self.sensor_id,
            "stictionFlagged": self.stiction_flagged,
            "decommissioned": self.decommissioned
        }

    def __repr__(self):
        return str(self.as_dict())

    @staticmethod
    def create(session, serial_number, sensor_id, stiction_flagged='0', decommissioned='0'):
        sensor = Sensors(serial_number=serial_number, sensor_id=sensor_id, stiction_flagged=stiction_flagged, decommissioned=decommissioned)
        session.add(sensor)
        session.commit()
        session.refresh(sensor)
        return sensor

    @staticmethod
    def get_by_id(session, id):
        sensor = session.query(Sensors)\
                        .filter_by(id=id)\
                        .first()
        return sensor

    @staticmethod
    def get_by_sensor_id(session, sensor_id):
        sensor = session.query(Sensors)\
                        .filter_by(id=sensor_id)\
                        .first()
        return sensor

    @staticmethod
    def update_by_id(session, id, sensor_id=None, serial_number=None, stiction_flagged=None, decommissioned=None):
        sensor = Sensors.get_by_id(session, id)
        if sensor_id is not None:
            sensor.sensor_id = sensor_id
        if serial_number is not None:
            sensor.serial_number = serial_number
        if stiction_flagged is not None:
            sensor.stiction_flagged = stiction_flagged
        if decommissioned is not None:
            sensor.decommissioned = decommissioned

        session.commit()
        session.refresh(sensor)
        return sensor

    @staticmethod
    def delete_by_sensor_id(session, sensor_id):
        sensor = Sensors.get_by_sensor_id(session, sensor_id)
        session.delete(sensor)
        session.commit()

    @staticmethod
    def delete_by_id(session, id):
        sensor = Sensors.get_by_id(session, id)
        session.delete(sensor)
        session.commit()
