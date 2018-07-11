import datetime
import os
import json

from sqlalchemy import ForeignKey, and_, or_, event
from sqlalchemy.orm import backref
from sqlalchemy.orm import object_session
from . import commit_or_rollback, db




tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column(
        'industrial_athlete_id',
        db.Integer,
        db.ForeignKey('industrial_athlete.id')
    ),
    db.UniqueConstraint('tag_id', 'industrial_athlete_id',)
)


groups = db.Table(
    'groups',
    db.Column('group_id', db.Integer, db.ForeignKey('athlete_group.id')),
    db.Column(
        'industrial_athlete_id',
        db.Integer,
        db.ForeignKey('industrial_athlete.id')
    ),
    db.UniqueConstraint('group_id', 'industrial_athlete_id',)
)


class IndustrialAthlete(db.Model):
    __tablename__ = 'industrial_athlete'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    client_id = db.Column(db.Integer, ForeignKey('client.id'), nullable=False)
    client = db.relationship(
        'Client',
        foreign_keys=client_id,
        backref='athletes'
    )
    gender = db.Column(db.String(1), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    external_id = db.Column(db.String(255), nullable=False)
    schedule = db.Column(db.String(255), nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    prior_back_injuries = db.Column(db.String(255), nullable=True)

    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('athletes')
    )
    athlete_groups = db.relationship(
        'Group',
        secondary=groups,
        backref=db.backref('athletes')
    )
    hire_date = db.Column(
        db.Date,
        default=datetime.date.today(),
        nullable=True
    )

    termination_date = db.Column(
        db.Date,
        nullable=True
    )

    warehouse_id = db.Column(
        db.Integer,
        ForeignKey('warehouse.id'),
        nullable=True
    )
    warehouse = db.relationship(
        'Warehouse',
        foreign_keys=warehouse_id,
        backref='athletes'
    )
    shift_id = db.Column(db.Integer, ForeignKey('shifts.id'), nullable=True)
    shift = db.relationship(
        'Shifts',
        foreign_keys=shift_id,
        backref='athletes'
    )
    job_function_id = db.Column(
        db.Integer,
        ForeignKey('job_function.id'),
        nullable=True
    )
    job_function = db.relationship(
        'JobFunction',
        foreign_keys=job_function_id,
        backref='athletes'
    )

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

    settings = db.Column(db.Text)
    
    def as_dict(self):
        return {
        "id": self.id,
        "warehouse_id": self.warehouse_id
    }

    @classmethod
    def get_warehouse_id(self, athlete_id):
        return db.session.query(
            IndustrialAthlete.warehouse_id
        ).filter(
            IndustrialAthlete.id == athlete_id
        ).scalar()


    def __repr__(self):
        return '%s@%s' % (self.id, self.client.id)


def get(athlete_id):
    return db.session.query(IndustrialAthlete).filter(
        IndustrialAthlete.id == athlete_id,
    ).scalar()



class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(255), nullable=False, unique=True)

    def __repr__(self):
        return self.name


class Group(db.Model):
    __tablename__ = 'athlete_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(255), nullable=False)
    group_administrator = db.Column(db.String(255), nullable=False)
    description = description = db.Column(db.Text(), nullable=True)
    client_id = db.Column(db.Integer, ForeignKey('client.id'), nullable=False)
    client = db.relationship(
        'Client',
        foreign_keys=client_id,
        backref='groups'
    )
    warehouse_id = db.Column(
        db.Integer,
        ForeignKey('warehouse.id'),
        nullable=True
    )
    warehouse = db.relationship(
        'Warehouse',
        foreign_keys=warehouse_id,
        backref='groups'
    )

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
        "warehouse_id": self.warehouse_id,
        "name": self.name,
    }

    def __repr__(self):
        return self.name

    db.UniqueConstraint('name', 'warehouse_id', name='name')