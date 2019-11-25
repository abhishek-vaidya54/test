import datetime

from sqlalchemy import ForeignKey

from . import db

class KeepaliveEvents(db.Model):
    __tablename__ = 'keepalive_events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    timestamp = db.Column(db.DateTime, nullable=False)
    event_type = db.Column(db.String(45), nullable=True, default=None)
    dockID = db.Column(db.String(45), nullable=True, default=None)
    db_inserted_at = db.Column(db.DateTime, nullable=True, default=None)
    batt_percent = db.Column(db.String(45), nullable=True, default=None)
    charge_status = db.Column(db.String(45), nullable=True, default=None)
    clientID = db.Column(db.String(50), nullable=True, default=None)
    warehouseID = db.Column(db.String(50), nullable=True, default=None)

    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.event_type,
            "dockID": self.dockID,
            "db_inserted_at": self.db_inserted_at,
            "batt_percent": self.batt_percent,
            "charge_status": self.charge_status,
            "clientID": self.clientID,
            "warehouseID": self.warehouseID
        }

    def __repr__(self):
        return 'keepalive event for dock %s' % (self.dockID)