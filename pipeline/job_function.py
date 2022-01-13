import datetime

from sqlalchemy import ForeignKey, and_, or_
from . import db


class JobFunction(db.Model):
    __tablename__ = "job_function"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    warehouse_id = db.Column(db.Integer, ForeignKey("warehouse.id"), nullable=False)
    warehouse = db.relationship(
        "Warehouse", foreign_keys=warehouse_id, backref="job_functions"
    )

    name = db.Column(db.String(255), nullable=False)
    max_package_mass = db.Column(db.FLOAT(), default=6.6)
    group_administrator = db.Column(db.String(255), nullable=False)
    max_package_weight = db.Column(db.Integer, nullable=True)
    min_package_weight = db.Column(db.Integer, nullable=True)
    avg_package_weight = db.Column(db.Integer, nullable=True)
    lbd_indicence = db.Column(db.Boolean, nullable=True, default=False)
    lbd_indicence_rate = db.Column(db.Integer(), nullable=True)
    description = db.Column(db.Text(), nullable=True)

    color = db.Column(db.String(255), nullable=True)

    db_created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    db_modified_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    standard_score = db.Column(db.Float)

    def as_dict(self):
        return {
            "id": self.id,
            "warehouse_id": self.warehouse_id,
            "name": self.name,
        }

    # __table_args__ = (db.UniqueConstraint('warehouse_id', 'color'), )

    def __repr__(self):
        return self.name


def get(job_function_id):
    return (
        db.session.query(JobFunction)
        .filter(
            JobFunction.id == job_function_id,
        )
        .one_or_none()
    )
