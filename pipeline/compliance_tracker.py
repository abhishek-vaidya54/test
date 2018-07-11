import datetime
from sqlalchemy import ForeignKey, event, func
from sqlalchemy.ext.hybrid import hybrid_property

from . import db


class EmailSchedule(db.Model):
    __tablename__ = 'email_schedule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Unicode(255), nullable=False)
    to_emails = db.Column(db.UnicodeText, nullable=False)
    pattern = db.Column(db.Unicode(255), nullable=False)
    pilot_length = db.Column(db.Integer, nullable=True, default = 10)

    group_id = db.Column(db.Integer, ForeignKey('athlete_group.id'), nullable=True)
    group = db.relationship(
        'Group',
        foreign_keys=group_id,
        backref='email_schedule_tests'
    )

    shift_id = db.Column(db.Integer, ForeignKey('shifts.id'), nullable=True)
    shift = db.relationship(
        'Shifts',
        foreign_keys=shift_id,
        backref='email_schedule_tests'
    )

    job_function_id = db.Column(
        db.Integer,
        ForeignKey('job_function.id'),
        nullable=True
    )
    job_function = db.relationship(
        'JobFunction',
        foreign_keys=job_function_id,
        backref='email_schedule_tests'
    )

    warehouse_id = db.Column(
        db.Integer,
        ForeignKey('warehouse.id'),
        nullable=False
    )
    warehouse = db.relationship(
        'Warehouse',
        foreign_keys=warehouse_id,
        backref='email_schedules'
    )

    client_id = db.Column(db.Integer, ForeignKey('client.id'), nullable=False)
    client = db.relationship(
        'Client',
        foreign_keys=client_id,
        backref='email_schedules'
    )

    db_created_at = db.Column(
        db.DateTime,
        server_default=func.current_timestamp(),
    )
    db_modified_at = db.Column(
        db.DateTime,
        server_default=func.current_timestamp(),
        onupdate=datetime.datetime.utcnow,
    )

    @hybrid_property
    def to_email_list(self):
        return self.to_emails.split(',') if self.to_emails else []

    def __repr__(self):
        return self.title


@event.listens_for(EmailSchedule, 'after_insert')
def signal_on_email_schedule_insert(mapper, connection, target):
    pass


@event.listens_for(EmailSchedule, 'after_update')
def signal_on_email_schedule_update(mapper, connection, target):
    pass
