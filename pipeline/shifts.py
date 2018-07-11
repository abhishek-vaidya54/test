import datetime
from sqlalchemy import ForeignKey, and_, or_

from . import db


class Shifts(db.Model):
    __tablename__ = 'shifts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    warehouse_id = db.Column(
        db.Integer,
        ForeignKey('warehouse.id'),
        nullable=False
    )
    warehouse = db.relationship(
        'Warehouse',
        foreign_keys=warehouse_id,
        backref='shifts'
    )

    name = db.Column(db.String(255), nullable=False)
    shift_start = db.Column(db.Time, nullable=False)
    shift_end = db.Column(db.Time, nullable=False)
    group_administrator = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    color = db.Column(db.String(255), nullable=True)

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

    # __table_args__ = (db.UniqueConstraint('warehouse_id', 'color'), )
    def is_match(self, time, warehouse_id = None):
        within_range = self.shift_start < time and self.shift_end > time
        if warehouse_id:
            check_warehouse = self.warehouse_id == warehouse_id
            return within_range and check_warehouse
        else:
            return within_range

    def __repr__(self):
        return 'shift %s' % (self.name, )
