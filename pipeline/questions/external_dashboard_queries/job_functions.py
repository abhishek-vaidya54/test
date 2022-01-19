import sqlalchemy as sa
from sqlalchemy import distinct

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


def warehouse_job_functions(warehouse_id):
    """Give all job functions of a given warehouse."""

    query = (
        db.db.session.query(
            db.JobFunction.id.label("id"),
            db.JobFunction.name.label("name"),
            db.JobFunction.color.label("color"),
        )
        .join(db.Warehouse)
        .filter(db.Warehouse.id == warehouse_id)
    )

    results = []
    for job_function in query:
        results.append(
            {
                "id": job_function.id,
                "name": job_function.name,
                "color": job_function.color,
            }
        )

    return results


def client_job_functions(client_guid, warehouse_id=None):
    """Give all job functions of a given client."""

    query = (
        db.db.session.query(
            db.JobFunction.id.label("id"),
            db.JobFunction.name.label("name"),
            db.JobFunction.color.label("color"),
        )
        .distinct(db.JobFunction.name)
        .join(db.Warehouse, db.Client)
        .filter(db.Client.guid == client_guid)
    )

    query = apply_warehouse_filter(
        query, warehouse_id, column=db.JobFunction.warehouse_id
    )

    results = []
    for job_function in query:
        results.append(
            {
                "id": job_function.id,
                "name": job_function.name,
                "color": job_function.color,
            }
        )

    return results


def job_functions(client_guid, range_start=None, range_end=None, warehouse_id=None):
    """Give the avg scores of each job functions on date range."""
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
            db.JobFunction.id.label("id"),
            db.JobFunction.name.label("name"),
            db.JobFunction.color.label("color"),
        )
        .join(db.ProcessedFile, db.Fuse, db.IndustrialAthlete, db.Warehouse, db.Client)
        .join(db.JobFunction, db.JobFunction.id == db.IndustrialAthlete.job_function_id)
        .filter(
            db.ProcessedFile.version == Config.ALGO_VERSION,
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
        .order_by("name", "day")
    )

    query = apply_warehouse_filter(
        query, warehouse_id, column=db.JobFunction.warehouse_id
    )

    data = [row for row in query]

    job_functions_scores = generate_daily_scores(data)

    client_job_functions = (
        db.db.session.query(db.JobFunction)
        .join(db.Warehouse, db.Client)
        .filter(db.Client.guid == client_guid)
    )

    client_job_functions = apply_warehouse_filter(
        client_job_functions, warehouse_id, column=db.JobFunction.warehouse_id
    )

    # fill the dict with empty scores list if no risk record found for any job
    # function.
    for client_job_function in client_job_functions:
        job_functions_scores.setdefault(
            client_job_function.id,
            job_functions_scores.get(
                client_job_function.id,
                {
                    "id": client_job_function.id,
                    "name": client_job_function.name,
                    "color": client_job_function.color,
                    "scores": [],
                },
            ),
        )

    return job_functions_scores


def job_functions_by_score(client_guid, sorting_order, warehouse_id=None):
    """Give the avg scores of highest/lowest risk."""

    query = (
        db.db.session.query(
            sa.func.avg(db.Risk.safety_score).label("safety_score"),
            sa.func.avg(db.Risk.avg_twist_velocity).label("avg_twist_velocity"),
            sa.func.avg(db.Risk.max_flexion).label("max_flexion"),
            sa.func.avg(db.Risk.max_moment).label("max_moment"),
            sa.func.avg(db.Risk.max_lateral_velocity).label("max_lateral_velocity"),
            sa.func.avg(db.Risk.lift_rate).label("lift_rate"),
            db.IndustrialAthlete.id.label("aid"),
            db.JobFunction.id.label("id"),
            db.JobFunction.name.label("name"),
        )
        .join(db.ProcessedFile, db.Fuse, db.IndustrialAthlete, db.Warehouse, db.Client)
        .join(db.JobFunction, db.JobFunction.id == db.IndustrialAthlete.job_function_id)
        .filter(
            db.ProcessedFile.version == Config.ALGO_VERSION,
            db.Client.guid == client_guid,
        )
        .group_by(
            db.JobFunction.id,
            db.IndustrialAthlete.id,
            db.ProcessedFile.id,
            db.Fuse.has_flx,
        )
    )

    query = apply_warehouse_filter(query, warehouse_id)
    return generate_scores(query, sorting_order)


def job_function_score(
    client_guid, jf_id, range_start=None, range_end=None, warehouse_id=None
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
            db.JobFunction.id.label("id"),
            db.JobFunction.name.label("name"),
            db.JobFunction.color.label("color"),
        )
        .join(db.ProcessedFile, db.Fuse, db.IndustrialAthlete, db.Warehouse, db.Client)
        .join(db.JobFunction, db.JobFunction.id == db.IndustrialAthlete.job_function_id)
        .filter(
            db.ProcessedFile.version == Config.ALGO_VERSION,
            db.Client.guid == client_guid,
            db.JobFunction.id == jf_id,
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
        .order_by("name", "day")
    )

    query = apply_warehouse_filter(
        query, warehouse_id, column=db.JobFunction.warehouse_id
    )

    data = [row for row in query]

    job_functions_scores = generate_daily_scores(data)

    client_job_functions = (
        db.db.session.query(db.JobFunction)
        .join(db.Warehouse, db.Client)
        .filter(
            db.Client.guid == client_guid,
            db.JobFunction.id == jf_id,
        )
    )

    client_job_functions = apply_warehouse_filter(
        client_job_functions, warehouse_id, column=db.JobFunction.warehouse_id
    )

    # fill the dict with empty scores list if no risk record found for any job
    # function.
    for client_job_function in client_job_functions:
        job_functions_scores.setdefault(
            client_job_function.id,
            job_functions_scores.get(
                client_job_function.id,
                {
                    "id": client_job_function.id,
                    "name": client_job_function.name,
                    "color": client_job_function.color,
                    "scores": [],
                },
            ),
        )

    return job_functions_scores
