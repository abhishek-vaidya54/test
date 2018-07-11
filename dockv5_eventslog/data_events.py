import datetime

from sqlalchemy import ForeignKey

from . import db

class DataEvents(db.Model):
    __tablename__ = 'data_events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    timestamp = db.Column(db.DateTime, nullable=True)
    type = db.Column(db.String(45), nullable=True)
    sensorID = db.Column(db.String(45), nullable=True)
    firmware_version = db.Column(db.String(45), nullable=True)
    datarecord_count = db.Column(db.Integer(20), nullable=True)
    db_inserted_at = db.Column(db.DateTime, nullable=True)
    assignment_time = db.Column(db.Integer(20), nullable=True)
    filename = db.Column(db.String(100), nullable=True)
    dockID = db.Column(db.String(45), nullable=True)
    warehouseID = db.Column(db.String(45), nullable=True)
    athleteID = db.Column(db.Integer, nullable=True)
    clientID = db.Column(db.Integer, nullable=True)
    port = db.Column(db.String(45), nullable=True)
    sessionID = db.Column(db.String(45), nullable=True)

    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.type,
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
        return 'dock %s for client %s' % (self.dock_id, self.client_id)