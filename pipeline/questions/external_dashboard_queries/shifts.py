import sqlalchemy as sa
from sqlalchemy import distinct
import logging

from pipeline.config import Config
from pipeline import db
from pipeline.db.questions.external_dashboard_queries.utils import (
    generate_scores,
    generate_daily_scores,
    get_date_range,
    apply_warehouse_filter,
)
from pipeline import date_time_utils as dtu

MONTH = 30


def shifts_by_score(client_guid, sorting_order, warehouse_id=None):
    query = (
        db.db.session.query(
            sa.func.avg(db.Risk.safety_score).label("safety_score"),
            sa.func.avg(db.Risk.max_flexion).label("max_flexion"),
            sa.func.avg(db.Risk.avg_twist_velocity).label("avg_twist_velocity"),
            sa.func.avg(db.Risk.max_moment).label("max_moment"),
            sa.func.avg(db.Risk.max_lateral_velocity).label("max_lateral_velocity"),
            sa.func.avg(db.Risk.lift_rate).label("lift_rate"),
            db.IndustrialAthlete.id.label("aid"),
            db.Shifts.id.label("id"),
            db.Shifts.name.label("name"),
        )
        .join(db.ProcessedFile, db.Fuse, db.IndustrialAthlete, db.Warehouse, db.Client)
        .join(db.Shifts, db.Shifts.id == db.IndustrialAthlete.shift_id)
        .filter(
            db.ProcessedFile.version == Config.ALGO_VERSION,
            db.Client.guid == client_guid,
        )
        .group_by(
            db.Shifts.id, db.IndustrialAthlete.id, db.ProcessedFile.id, db.Fuse.has_flx
        )
    )

    query = apply_warehouse_filter(query, warehouse_id)

    return generate_scores(query, sorting_order)


def shifts(client_guid, range_start=None, range_end=None, warehouse_id=None):
    range_start, range_end = get_date_range(client_guid, range_start, range_end)
    query = (
        db.db.session.query(
            sa.func.avg(db.Risk.safety_score).label("safety_score"),
            sa.func.avg(db.Risk.avg_twist_velocity).label("avg_twist_velocity"),
            sa.func.avg(db.Risk.max_flexion).label("max_flexion"),
            sa.func.avg(db.Risk.max_moment).label("max_moment"),
            sa.func.avg(db.Risk.max_lateral_velocity).label("max_lateral_velocity"),
            sa.func.avg(db.Risk.lift_rate).label("lift_rate"),
            sa.func.DATE(
                dtu.convert_tz(
                    db.ProcessedFile.start_time,
                    db.UTC_TIMEZONE,
                    db.Warehouse.prefered_timezone,
                )
            ).label("day"),
            db.IndustrialAthlete.id.label("aid"),
            db.IndustrialAthlete.name.label("athlete_name"),
            sa.func.DATE(
                dtu.convert_tz(
                    db.IndustrialAthlete.hire_date,
                    db.UTC_TIMEZONE,
                    db.Warehouse.prefered_timezone,
                )
            ).label("athlete_hire_date"),
            db.Shifts.id.label("id"),
            db.Shifts.name.label("name"),
            db.Shifts.color.label("color"),
        )
        .join(db.ProcessedFile, db.Fuse, db.IndustrialAthlete, db.Warehouse, db.Client)
        .join(db.Shifts, db.Shifts.id == db.IndustrialAthlete.shift_id)
        .filter(db.ProcessedFile.version == Config.ALGO_VERSION)
        .filter(
            db.Client.guid == client_guid,
            sa.func.DATE(
                dtu.convert_tz(
                    db.ProcessedFile.start_time,
                    db.UTC_TIMEZONE,
                    db.Warehouse.prefered_timezone,
                )
            )
            >= range_start,
            sa.func.DATE(
                dtu.convert_tz(
                    db.ProcessedFile.end_time,
                    db.UTC_TIMEZONE,
                    db.Warehouse.prefered_timezone,
                )
            )
            <= range_end,
        )
        .group_by(db.IndustrialAthlete.id, db.ProcessedFile.id, db.Fuse.has_flx)
        .order_by("id", "day")
    )

    query = apply_warehouse_filter(query, warehouse_id, column=db.Shifts.warehouse_id)

    data = [row for row in query]

    shifts_scores = generate_daily_scores(data)

    client_shifts = (
        db.db.session.query(db.Shifts)
        .join(db.Warehouse, db.Client)
        .filter(db.Client.guid == client_guid)
    )

    client_shifts = apply_warehouse_filter(
        client_shifts, warehouse_id, column=db.Shifts.warehouse_id
    )

    # fill the dict with empty scores list if no risk record found for any
    # shift.
    for client_shift in client_shifts:
        shifts_scores.setdefault(
            client_shift.id,
            shifts_scores.get(
                client_shift.id,
                {
                    "id": client_shift.id,
                    "name": client_shift.name,
                    "color": client_shift.color,
                    "scores": [],
                },
            ),
        )

    return shifts_scores


def shift_score(
    client_guid, shift_id, range_start=None, range_end=None, warehouse_id=None
):
    range_start, range_end = get_date_range(client_guid, range_start, range_end)
    query = (
        db.db.session.query(
            sa.func.avg(db.Risk.safety_score).label("safety_score"),
            sa.func.avg(db.Risk.avg_twist_velocity).label("avg_twist_velocity"),
            sa.func.avg(db.Risk.max_flexion).label("max_flexion"),
            sa.func.avg(db.Risk.max_moment).label("max_moment"),
            sa.func.avg(db.Risk.max_lateral_velocity).label("max_lateral_velocity"),
            sa.func.avg(db.Risk.lift_rate).label("lift_rate"),
            sa.func.DATE(
                dtu.convert_tz(
                    db.ProcessedFile.start_time,
                    db.UTC_TIMEZONE,
                    db.Warehouse.prefered_timezone,
                )
            ).label("day"),
            db.IndustrialAthlete.id.label("aid"),
            db.IndustrialAthlete.name.label("athlete_name"),
            sa.func.DATE(
                dtu.convert_tz(
                    db.IndustrialAthlete.hire_date,
                    db.UTC_TIMEZONE,
                    db.Warehouse.prefered_timezone,
                )
            ).label("athlete_hire_date"),
            db.Shifts.id.label("id"),
            db.Shifts.name.label("name"),
            db.Shifts.color.label("color"),
        )
        .join(db.ProcessedFile, db.Fuse, db.IndustrialAthlete, db.Warehouse, db.Client)
        .join(db.Shifts, db.Shifts.id == db.IndustrialAthlete.shift_id)
        .filter(db.ProcessedFile.version == Config.ALGO_VERSION)
        .filter(
            db.Client.guid == client_guid,
            db.Shifts.id == shift_id,
            sa.func.DATE(
                dtu.convert_tz(
                    db.ProcessedFile.start_time,
                    db.UTC_TIMEZONE,
                    db.Warehouse.prefered_timezone,
                )
            )
            >= range_start,
            sa.func.DATE(
                dtu.convert_tz(
                    db.ProcessedFile.end_time,
                    db.UTC_TIMEZONE,
                    db.Warehouse.prefered_timezone,
                )
            )
            <= range_end,
        )
        .group_by(db.IndustrialAthlete.id, db.ProcessedFile.id, db.Fuse.has_flx)
        .order_by("id", "day")
    )

    query = apply_warehouse_filter(query, warehouse_id, column=db.Shifts.warehouse_id)

    data = [row for row in query]
    logging.info(data)

    shifts_scores = generate_daily_scores(data)

    client_shifts = (
        db.db.session.query(db.Shifts)
        .join(db.Warehouse, db.Client)
        .filter(db.Client.guid == client_guid)
        .filter(db.Shifts.id == shift_id)
    )

    client_shifts = apply_warehouse_filter(
        client_shifts, warehouse_id, column=db.Shifts.warehouse_id
    )

    # fill the dict with empty scores list if no risk record found for any
    # shift.
    for client_shift in client_shifts:
        shifts_scores.setdefault(
            client_shift.id,
            shifts_scores.get(
                client_shift.id,
                {
                    "id": client_shift.id,
                    "name": client_shift.name,
                    "color": client_shift.color,
                    "scores": [],
                },
            ),
        )

    return shifts_scores


def list_shifts(client_guid, warehouse_id=None):
    query = (
        db.db.session.query(db.Shifts)
        .join(db.Warehouse, db.Client)
        .filter(db.Client.guid == client_guid)
    )

    query = apply_warehouse_filter(query, warehouse_id, column=db.Shifts.warehouse_id)

    data = [row for row in query]

    rows = []

    for row in data:
        rows.append(
            {
                "id": row.id,
                "name": row.name,
                "shift_start": row.shift_start.isoformat(),
                "shift_end": row.shift_end.isoformat(),
            }
        )

    return rows
