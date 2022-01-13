import datetime

from sqlalchemy import ForeignKey

from . import db


class Dockv5AppcrashLog(db.Model):
    __tablename__ = "dockv5_appcrash_log"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    timestamp = db.Column(db.DateTime, nullable=False)
    log = db.Column(db.String(5000), nullable=False)
    dockID = db.Column(db.String(12), nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "log": self.log,
            "dockID": self.dockID,
        }

    def __repr__(self):
        return "Dock %s Log: %s" % (self.dockID, self.log)
