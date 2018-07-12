import datetime

from sqlalchemy import ForeignKey

from . import db

class EngagementStats(db.Model):
    __tablename__ = 'engagement_stats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    athlete_id = db.Column(db.Integer(11), unique=True, nullable=False)
    total_days_worn = db.Column(db.Integer(11), nullable=True, default='0')
    total_hours_worn = db.Column(db.Integer(11), nullable=True, default='0')

    last_checkin = db.Column(db.DateTime, nullable=True, default=None)
    last_checkout = db.Column(db.DateTime, nullable=True, default=None)
    db_created_at = db.Column(db.DateTime, nullable=True, default=None)
    db_modified_at = db.Column(db.DateTime, nullable=True, default=None)

    def as_dict(self):
        return {
            "id": self.id,
            "athlete_id": self.athlete_id,
            "total_days_worn": self.total_days_worn,
            "total_hours_worn": self.total_hours_worn,
            "last_checkin": self.last_checkin,
            "last_checkout": self.last_checkout,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at
        }

    def __repr__(self):
        return '%d days worn for athleteID: %s' % (self.total_days_worn, self.athlete_id)