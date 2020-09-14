import datetime

from sqlalchemy import ForeignKey

from . import db


class Warehouse(db.Model):
    __tablename__ = 'warehouse'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 
    client_id = db.Column(db.Integer, ForeignKey('client.id'), nullable=False)
    client = db.relationship(
        'Client',
        foreign_keys=client_id,
        backref='warehouses'
    )

    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(500), nullable=True)
    prefered_timezone = db.Column(
        db.String(100),
        server_default='UTC',
        nullable=False
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

    algo_version = db.Column(db.Integer, nullable=True)
    display_names = db.Column(db.Boolean, nullable=False)

    utc_op_day_start = db.Column(db.String(45), nullable=False)

    week_start = db.Column(db.String(45), nullable=False)

    update_engagement = db.Column(
        db.Integer,
        default=1, 
        nullable=False
    )

    standard_score = db.Column(db.Float, nullable=True)
    min_safety_score = db.Column(db.Float, nullable=True)
    max_safety_score = db.Column(db.Float, nullable=True)
    first_quarter_safety_score = db.Column(db.Float, nullable=True)
    median_safety_score = db.Column(db.Float, nullable=True)
    third_quarter_safety_score = db.Column(db.Float, nullable=True)


    def as_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "name": self.name,
            "location": self.location,
            "prefered_timezone": self.prefered_timezone,
            "warehouse_regex_code": self.client.client_regex_code
        }

    def __repr__(self):
        return 'warehouse %s for client %s' % (self.name, self.client.name)


class Masquerade(db.Model):
    __tablename__ = 'masquerade'
    __table_args__ = (db.UniqueConstraint('original_warehouse_id', ),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enable = db.Column(db.Boolean, nullable=False, default=False)
    original_warehouse_id = db.Column(
        db.Integer,
        ForeignKey('warehouse.id'),
        nullable=True
    )
    original_warehouse = db.relationship(
        'Warehouse',
        foreign_keys=original_warehouse_id,
        backref='masqurades'
    )

    masquerade_warehouse_id = db.Column(
        db.Integer,
        ForeignKey('warehouse.id'),
        nullable=True
    )
    masquerade_warehouse = db.relationship(
        'Warehouse',
        foreign_keys=masquerade_warehouse_id,
        backref='masquerade'
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
