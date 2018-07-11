import datetime

import json
import sqlalchemy as sa
from sqlalchemy import ForeignKey, and_, or_, event
from sqlalchemy.orm import backref
from sqlalchemy.orm import object_session
from . import commit_or_rollback, db

class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entity_type = db.Column(db.String(255), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(255), nullable=False)
    before_state = db.Column(db.Text(), nullable=True)
    after_state = db.Column(db.Text(), nullable=True)
    
    client_id = db.Column(db.Integer, ForeignKey('client.id'), nullable=False)
    client = db.relationship(
        'Client',
        foreign_keys=client_id,
        backref='activities'
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

    @staticmethod
    def list_activities(entity_type, entity_id=None, offset=None, limit=None):
        query = db.session.query(Activity)

        if entity_id is not None:
            query = query.filter(
                Activity.entity_id == entity_id
            )

        if offset is not None and limit is not None:
            query = query.offset(offset).limit(limit)

        data = [row for row in query]

        rows = []

        for row in data:
            activity = {
                "id": row.id,
                "entity_type": row.entity_type,
                "entity_id": row.entity_id,
                "action": row.action,
                "before_state": row.before_state,
                "after_state": row.after_state,
                "created_at": row.db_created_at,
                "modified_at": row.db_modified_at
            }

            rows.append(activity)

        count = Activity.count_activities(entity_type, entity_id)

        result = {"total": count, "rows": rows}

        return result

    @staticmethod
    def count_activities(entity_type, entity_id=None):
        query = db.session.query(sa.func.count("*")).select_from(Activity)

        if entity_id is not None:
            query = query.filter(
                Activity.entity_id == entity_id
            )

            return query.scalar()

    @staticmethod
    def save_activity(user_id, client_id, entity_type, entity_id, action, before_state=None, after_state=None):
        activity = Activity(
            user_id=user_id,
            client_id=client_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            before_state=before_state,
            after_state=after_state,
            db_created_at=datetime.datetime.now(),
            db_modified_at=datetime.datetime.now()
        )
        db.session.add(activity)
        db.session.commit()
