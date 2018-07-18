import datetime
from . import db


class JobFunction(db.Model):
    __tablename__ = 'monthly_safety'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    athlete_id = db.Column(db.Integer(), nullable=False)
    latest_safety_score = db.Column(db.FLOAT(), default=0.0)
    monthly_score = db.Column(db.FLOAT(), nullable=False, default=0.0)
    safety_standard = db.Column(db.FLOAT(), nullable=True, default=70.0)
    status = db.Column(db.Text(), nullable=False)
    color = db.Column(db.Text(), nullable=True, default='#0CB074')

    db_created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    db_modified_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )


    def as_dict(self):
        return {
            "id": self.id,
            "athlete_id": self.athlete_id,
            "monthly_score": self.monthly_score,
        }

    def __repr__(self):
        return self.name

