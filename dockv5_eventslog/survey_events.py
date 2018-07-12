import datetime

from sqlalchemy import ForeignKey

from . import db

class SurveyEvents(db.Model):
    __tablename__ = 'survey_events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    timestamp = db.Column(db.DateTime, nullable=False)
    event_type = db.Column(db.String(45), nullable=True, default=None)
    athleteID = db.Column(db.String(45), nullable=True, default=None)
    dockID = db.Column(db.String(45), nullable=True, default=None)
    survey_type = db.Column(db.String(45), nullable=True, default=None)
    response = db.Column(db.String(45), nullable=True, default=None)
    db_inserted_at = db.Column(db.DateTime, nullable=True, default=None)
    firmware_version = db.Column(db.String(45), nullable=True, default=None)
    clientID = db.Column(db.String(50), nullable=True, default=None)
    warehouseID = db.Column(db.String(50), nullable=True, default=None)
    
    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.event_type,
            "athleteID": self.athleteID,
            "dockID": self.dockID,
            "survey_type": self.survey_type,
            "response": self.response,
            "db_inserted_at": self.db_inserted_at,
            "firmware_version": self.firmware_version,
            "clientID": self.clientID,
            "warehouseID": self.warehouseID  
        }

    def __repr__(self):
        return 'survey events. for %s, response is: %s' % (self.survey_type, self.response)