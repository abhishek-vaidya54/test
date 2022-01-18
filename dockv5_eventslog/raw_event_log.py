import datetime

from sqlalchemy import ForeignKey

from . import db


class RawEventLog(db.Model):
    __tablename__ = "raw_event_log"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    timestamp = db.Column(db.DateTime, nullable=False)
    event_type = db.Column(db.String(255), nullable=True, default=None)
    dockID = db.Column(db.String(45), nullable=True, default=None)
    assignment_time = db.Column(db.Integer(20), nullable=True, default=None)
    clientID = db.Column(db.String(50), nullable=True, default=None)
    warehouseID = db.Column(db.String(50), nullable=True, default=None)
    sensorID = db.Column(db.String(50), nullable=True, default=None)
    athleteID = db.Column(db.String(50), nullable=True, default=None)
    datarecord_count = db.Column(db.Integer(20), nullable=True, default=None)
    db_inserted_at = db.Column(db.DateTime, nullable=False)
    port = db.Column(db.Integer(11), nullable=True, default=None)
    firmware_version = db.Column(db.String(45), nullable=True, default=None)
    survey_type = db.Column(db.String(45), nullable=True, default=None)
    filename = db.Column(db.String(45), nullable=True, default=None)
    batt_percent = db.Column(db.String(45), nullable=True, default=None)
    charge_status = db.Column(db.String(45), nullable=True, default=None)
    event_blob = db.Column(db.String(1000), nullable=True, default=None)
    sessionID = db.Column(db.String(45), nullable=True, default=None)

    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.event_type,
            "dockID": self.dockID,
            "assignment_time": self.assignment_time,
            "clientID": self.clientID,
            "warehouseID": self.warehouseID,
            "sensorID": self.sensorID,
            "athleteID": self.athleteID,
            "datarecord_count": self.datarecord_count,
            "db_inserted_at": self.db_inserted_at,
            "port": self.port,
            "firmware_version": self.firmware_version,
            "survey_type": self.survey_type,
            "filename": self.filename,
            "batt_percent": self.batt_percent,
            "charge_status": self.charge_status,
            "event_blob": self.event_blob,
            "sessionID": self.sessionID,
        }

    def __repr__(self):
        return "raw event log. event type: %s" % (self.event_type)
