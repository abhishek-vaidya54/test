import datetime

from sqlalchemy import ForeignKey

from . import db

class Config(db.Model):
    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    dock_id = db.Column(db.String(45), nullable=False)
    client_id = db.Column(db.Integer, nullable=True)
    warehouse_id = db.Column(db.Integer, nullable=True)
    deployment_stage = db.Column(db.String(45), nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "dock_id": self.dock_id,
            "client_id": self.client_id,
            "warehouse_id": self.warehouse_id,
            "deployment_stage": self.deployment_stage
        }

    def __repr__(self):
        return 'dock %s for client %s' % (self.dock_id, self.client_id)