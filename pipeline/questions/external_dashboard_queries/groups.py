import sqlalchemy as sa
from pipeline import db
from pipeline.config import Config

from pipeline.db.questions.external_dashboard_queries.utils import apply_warehouse_filter
from pipeline.db.questions.external_dashboard_queries.utils import generate_scores, generate_daily_scores, get_date_range
from pipeline import date_time_utils as dtu


def client_groups(client_guid, warehouse_id=None):
    query = db.db.session.query(
        db.Group
    ).join(db.Client).filter(db.Client.guid == client_guid)

    query = apply_warehouse_filter(query, warehouse_id, column=db.Group.warehouse_id)

    results = []
    for group in query:
        results.append(
            {
                "id": group.id,
                "name": group.name
            }
        )

    return results

def custom_groups(client_guid, range_start=None, range_end=None, warehouse_id= None):
    range_start, range_end = get_date_range(client_guid, range_start, range_end)
    query = db.db.session.query(
        sa.func.avg(db.Risk.safety_score).label('safety_score'),
        sa.func.avg(db.Risk.avg_twist_velocity).label('avg_twist_velocity'),
        sa.func.avg(db.Risk.max_flexion).label('max_flexion'),
        sa.func.avg(db.Risk.max_moment).label('max_moment'),
        sa.func.avg(db.Risk.max_lateral_velocity).label('max_lateral_velocity'),
        sa.func.avg(db.Risk.lift_rate).label('lift_rate'),
        sa.func.DATE(
            dtu.convert_tz(
                db.ProcessedFile.start_time,
                db.UTC_TIMEZONE,
                db.Warehouse.prefered_timezone
            )
        ).label('day'),
        db.IndustrialAthlete.id.label('aid'),
        db.IndustrialAthlete.name.label('athlete_name'),
        sa.func.DATE(
            dtu.convert_tz(
                db.IndustrialAthlete.hire_date,
                db.UTC_TIMEZONE,
                db.Warehouse.prefered_timezone
            )
        ).label('athlete_hire_date'),
        db.Group.id.label('id'),
        db.Group.name.label('name')
    ).join(
        db.ProcessedFile,
        db.Fuse,
        db.IndustrialAthlete,
        db.Warehouse,
        db.Client,
        db.groups
    ).join(
        db.Group, db.Group.id == db.groups.c.group_id
    ).filter(
        db.ProcessedFile.version == Config.ALGO_VERSION
    ).filter(
        db.Client.guid == client_guid,
        sa.func.DATE(
            dtu.convert_tz(
                db.ProcessedFile.start_time,
                db.UTC_TIMEZONE,
                db.Warehouse.prefered_timezone)) >= range_start,
        sa.func.DATE(
            dtu.convert_tz(
                db.ProcessedFile.end_time,
                db.UTC_TIMEZONE,
                db.Warehouse.prefered_timezone)) <= range_end
    ).group_by(
        db.IndustrialAthlete.id,
        db.Group.id,
        db.ProcessedFile.id,
        db.Fuse.has_flx
    ).order_by('id', 'day')

    query = apply_warehouse_filter(query, warehouse_id, column=db.Group.warehouse_id)

    data = [row for row in query]

    groups_scores = generate_daily_scores(data)

    client_groups = db.db.session.query(
        db.Group
    ).join(
        db.Warehouse, db.Client
    ).filter(
        db.Client.guid == client_guid
    )

    client_groups = apply_warehouse_filter(client_groups, warehouse_id, column=db.Group.warehouse_id)

    # fill the dict with empty scores list if no risk record found for any
    # group
    for client_group in client_groups:
        groups_scores.setdefault(
            client_group.id, groups_scores.get(client_group.id, {
                "id": client_group.id,
                "name": client_group.name,
                "scores": []
            })
        )

    return groups_scores

def custom_group_score(client_guid, group_id, range_start=None, range_end=None, warehouse_id= None):
    range_start, range_end = get_date_range(client_guid, range_start, range_end)
    query = db.db.session.query(
        sa.func.avg(db.Risk.safety_score).label('safety_score'),
        sa.func.avg(db.Risk.avg_twist_velocity).label('avg_twist_velocity'),
        sa.func.avg(db.Risk.max_flexion).label('max_flexion'),
        sa.func.avg(db.Risk.max_moment).label('max_moment'),
        sa.func.avg(db.Risk.max_lateral_velocity).label('max_lateral_velocity'),
        sa.func.avg(db.Risk.lift_rate).label('lift_rate'),
        sa.func.DATE(
            dtu.convert_tz(
                db.ProcessedFile.start_time,
                db.UTC_TIMEZONE,
                db.Warehouse.prefered_timezone
            )
        ).label('day'),
        db.IndustrialAthlete.id.label('aid'),
        db.IndustrialAthlete.name.label('athlete_name'),
        sa.func.DATE(
            dtu.convert_tz(
                db.IndustrialAthlete.hire_date,
                db.UTC_TIMEZONE,
                db.Warehouse.prefered_timezone
            )
        ).label('athlete_hire_date'),
        db.Group.id.label('id'),
        db.Group.name.label('name')
    ).join(
        db.ProcessedFile,
        db.Fuse,
        db.IndustrialAthlete,
        db.Warehouse,
        db.Client,
        db.groups
    ).join(
        db.Group, db.Group.id == db.groups.c.group_id
    ).filter(
        db.ProcessedFile.version == Config.ALGO_VERSION
    ).filter(
        db.Client.guid == client_guid,
        db.Group.id == group_id,
        sa.func.DATE(
            dtu.convert_tz(
                db.ProcessedFile.start_time,
                db.UTC_TIMEZONE,
                db.Warehouse.prefered_timezone)) >= range_start,
        sa.func.DATE(
            dtu.convert_tz(
                db.ProcessedFile.end_time,
                db.UTC_TIMEZONE,
                db.Warehouse.prefered_timezone)) <= range_end
    ).group_by(
        db.IndustrialAthlete.id,
        db.Group.id,
        db.ProcessedFile.id,
        db.Fuse.has_flx
    ).order_by('id', 'day')

    query = apply_warehouse_filter(query, warehouse_id, column=db.Group.warehouse_id)

    data = [row for row in query]

    groups_scores = generate_daily_scores(data)

    client_groups = db.db.session.query(
        db.Group
    ).join(
        db.Warehouse, db.Client
    ).filter(
        db.Client.guid == client_guid,
        db.Group.id == group_id
    )

    client_groups = apply_warehouse_filter(client_groups, warehouse_id, column=db.Group.warehouse_id)

    # fill the dict with empty scores list if no risk record found for any
    # group
    for client_group in client_groups:
        groups_scores.setdefault(
            client_group.id, groups_scores.get(client_group.id, {
                "id": client_group.id,
                "name": client_group.name,
                "scores": []
            })
        )

    return groups_scores