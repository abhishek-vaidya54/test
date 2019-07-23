"""show_engagement and hide_judgement removed from warehouse table and added to settings blob

Revision ID: f4daaa2c2953
Revises: 5ebe016d83da
Create Date: 2019-07-09 12:44:55.057322

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TINYINT
import datetime

Base = declarative_base()

# revision identifiers, used by Alembic.
revision = 'f4daaa2c2953'
down_revision = '5ebe016d83da'
branch_labels = None
depends_on = None

class Warehouse(Base):
    __tablename__ = 'warehouse'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    hide_judgement = sa.Column(TINYINT, nullable=False)
    show_engagement = sa.Column(TINYINT, nullable=False)

class Groups(Base):
    __tablename__ = 'groups'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String)

class IndustrialAthlete(Base):
    __tablename__ = 'industrial_athlete'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    group_id = sa.Column(sa.Integer, sa.ForeignKey('groups.id'))
    setting_id = sa.Column(sa.Integer, sa.ForeignKey('settings.id'))
    warehouse_id = sa.Column(sa.Integer, sa.ForeignKey('warehouse.id'), nullable=True)

class Settings(Base):
    __tablename__ = 'settings'
    
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    target_id = sa.Column(sa.Integer, nullable=False)
    target_type = sa.Column(sa.Text, nullable=False)
    value = sa.Column(sa.JSON)  
    db_created_at = sa.Column(
        sa.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )

def upgrade():

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    default_value = {
        u'athleteEnabled': False,
        u'enagementEnabled': False,
        u'eulaVersion': 0,
        u'hapticBendNumber': 0,
        u'hapticBendPercentile': 0,
        u'hapticEnabled': False,
        u'hapticFeedbackGap': 0,
        u'hapticFeedbackWindow': 0,
        u'hapticSagAngleThreshold': 0,
        u'hapticSingleBendWindow': 0,
        u'showBaselineModal': False,
        u'showEngagement': False,
        u'showHapticModal': False,
        u'showSafetyJudgement': True,
        u'showSafetyScoreModal': False
    }

    def convert_value_from_string(value, defaults=default_value):
        copyValue = value.copy()
        for key in copyValue:
            v = copyValue[key]
            if type(v) == unicode:
                if v.lower() == u'true':
                    copyValue[key] = True
                elif v.lower() == u'false':
                    copyValue[key] = False
                else:
                    try:
                        copyValue[key] = int(v)
                    except ValueError:
                        pass
        for key in defaults:
            copyValue[key] = copyValue.get(key, defaults[key])
        return copyValue

    new_settings_entries = []

    for warehouse in session.query(Warehouse):
        setting = session.query(Settings).\
            filter(Settings.target_type == 'warehouse', Settings.target_id == warehouse.id).\
            order_by(Settings.db_created_at.desc()).\
            first()
        if setting:
            value = setting.value
        else:
            value = default_value
        value[u'showEngagement'] = warehouse.show_engagement == 1
        value[u'showSafetyJudgement'] = warehouse.hide_judgement == 0
        value = convert_value_from_string(value)
        new_settings_entries.append(Settings(
            target_type = 'warehouse',
            target_id = warehouse.id,
            value = value
        ))
    
    for athlete in session.query(IndustrialAthlete):
        if athlete.setting_id:
            setting = session.query(Settings).\
                filter(Settings.id == athlete.setting_id).\
                one()
            value = setting.value
            warehouse = session.query(Warehouse).\
                filter(Warehouse.id == athlete.warehouse_id).\
                one_or_none()
            if warehouse:
                value[u'showEngagement'] = warehouse.show_engagement == 1
                value[u'showSafetyJudgement'] = warehouse.hide_judgement == 0
                value = convert_value_from_string(value)
                new_settings_entries.append(Settings(
                    target_type = 'athlete',
                    target_id = athlete.id,
                    value = value
                ))

    for group in session.query(Groups):
        warehouses = {}
        for athlete in session.query(IndustrialAthlete).filter(IndustrialAthlete.group_id == group.id):
            if athlete.warehouse_id not in warehouses:
                warehouses[athlete.warehouse_id] = session.query(Warehouse).\
                    filter(Warehouse.id == athlete.warehouse_id).one()
        if len(warehouses) == 0:
            # No warehouses to copy columns from.  Skip
            continue
        if len(warehouses) > 1:
            # Make sure that they all have the same settings
            show_engagements =  {True: [], False: []}
            hide_judgements =   {True: [], False: []}
            for warehouse_id in warehouses:
                warehouse = warehouses[warehouse_id]
                show_engagements[warehouse.show_engagement == 1].append(warehouse)
                hide_judgements[warehouse.hide_judgement == 1].append(warehouse)
            if len(show_engagements[True]) > 0 and len(show_engagements[False]) > 0:
                continue
                # Warehouses don't have the same settings for show_engagement
                raise Exception(
                    "Group {} spans warehouses {} that don't have the same show_engagement setting".\
                        format(group.id, warehouses.keys()))
            if len(hide_judgements[True]) > 0 and len(hide_judgements[False]) > 0:
                continue
                # Warehouses don't have the same settings for hide_judgement
                raise Exception(
                    "Group {} spans warehouses {} that don't have the same hide_judgement setting".\
                        format(group.id, warehouses.keys()))
            # Warehouses here share the same setting for both columns
            show_engagement = True if len(show_engagements[True]) > 0 else False
            show_safety_judgement = False if len(hide_judgements[True]) > 0 else True
        else:
            # Only 1 warehouse in the group, safe to copy over columns
            warehouse = warehouses.values()[0]
            show_engagement = warehouse.show_engagement == 1
            show_safety_judgement = warehouse.hide_judgement == 0
        setting = session.query(Settings).\
            filter(Settings.target_type == 'group', Settings.target_id == group.id).\
            order_by(Settings.db_created_at.desc()).\
            first()
        value = setting.value
        value[u'showEngagement'] = show_engagement
        value[u'showSafetyJudgement'] = show_safety_judgement
        value = convert_value_from_string(value)
        new_settings_entries.append(Settings(
            target_type = 'group',
            target_id = group.id,
            value = value
        ))

    session.add_all(new_settings_entries)
    session.commit()

    op.drop_column('warehouse', 'show_engagement')
    op.drop_column('warehouse', 'hide_judgement')

def downgrade():

    op.add_column('warehouse', sa.Column('show_engagement', TINYINT, default=0))
    op.add_column('warehouse', sa.Column('hide_judgement', TINYINT, default=0))

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # Copy show_engagement and hide_judgement from settings blob to columns
    for warehouse in session.query(Warehouse):
        setting = session.query(Settings).\
            filter(Settings.target_type == 'warehouse', Settings.target_id == warehouse.id).\
            order_by(Settings.db_created_at.desc()).\
            first()
        if setting:
            value = setting.value
            warehouse.show_engagement = 1 if value.get(u'showEngagement', False) else 0
            warehouse.hide_judgement = 0 if value.get(u'showSafetyJudgement', True) else 1

    session.commit()