import datetime

from sqlalchemy import ForeignKey

from . import db

class DataEvents(db.Model):
    __tablename__ = 'data_events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    timestamp = db.Column(db.DateTime, nullable=True, default=None)
    event_type = db.Column(db.String(45), nullable=True, default=None)
    sensorID = db.Column(db.String(45), nullable=True, default=None)
    firmware_version = db.Column(db.String(45), nullable=True, default=None)
    datarecord_count = db.Column(db.Integer(20), nullable=True, default=None)
    db_inserted_at = db.Column(db.DateTime, nullable=True, default=None)
    assignment_time = db.Column(db.Integer(20), nullable=True, default=None)
    filename = db.Column(db.String(100), nullable=True, default=None)
    dockID = db.Column(db.String(45), nullable=True, default=None)
    warehouseID = db.Column(db.String(45), nullable=True, default=None)
    athleteID = db.Column(db.Integer, nullable=True, default=None)
    clientID = db.Column(db.Integer, nullable=True, default=None)
    port = db.Column(db.String(45), nullable=True, default=None)
    sessionID = db.Column(db.String(45), nullable=True, default=None)

    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.event_type,
            "sensorID": self.sensorID,
            "firmware_version": self.firmware_version,
            "datarecord_count": self.datarecord_count,
            "db_inserted_at": self.db_inserted_at,
            "assignment_time": self.assignment_time,
            "filename": self.filename,
            "dockID": self.dockID,
            "warehouseID": self.warehouseID,
            "athleteID": self.athleteID,
            "clientID": self.clientID,
            "port": self.port,
            "sessionID": self.sessionID
        }

    def __repr__(self):
        return 'event type: %s' % (self.event_type)