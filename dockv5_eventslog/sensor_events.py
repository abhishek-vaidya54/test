import datetime

from sqlalchemy import ForeignKey

from . import db


class SensorEvents(db.Model):
    __tablename__ = "sensor_events"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    timestamp = db.Column(db.DateTime, nullable=False)
    event_type = db.Column(db.String(45), nullable=True, default=None)
    dockID = db.Column(db.String(45), nullable=True, default=None)
    clientID = db.Column(db.String(45), nullable=True, default=None)
    warehouseID = db.Column(db.String(45), nullable=True, default=None)
    assignment_time = db.Column(db.Integer(20), nullable=True, default=None)
    sensorID = db.Column(db.String(45), nullable=True, default=None)
    athleteID = db.Column(db.String(45), nullable=True, default=None)
    datarecord_count = db.Column(db.Integer(20), nullable=True, default=None)
    port = db.Column(db.Integer(11), nullable=True, default=None)
    db_inserted_at = db.Column(db.DateTime, nullable=False)
    firmware_version = db.Column(db.String(45), nullable=True, default=None)
    sessionID = db.Column(db.String(45), nullable=True, default=None)

    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.event_type,
            "dockID": self.dockID,
            "clientID": self.clientID,
            "warehouseID": self.warehouseID,
            "assignment_time": self.assignment_time,
            "sensorID": self.sensorID,
            "athleteID": self.athleteID,
            "datarecord_count": self.datarecord_count,
            "port": self.port,
            "db_inserted_at": self.db_inserted_at,
            "firmware_version": self.firmware_version,
            "sessionID": self.sessionID,
        }

    def __repr__(self):
        return "sensor events. event type: %s" % (self.event_type)
