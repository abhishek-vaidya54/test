import datetime
import copy
import operator
import json
import logging
import requests
from requests.exceptions import ConnectionError, Timeout
import sqlalchemy as sa
from sqlalchemy.sql import text
from sqlalchemy.orm import joinedload, subqueryload
from sqlalchemy.orm.exc import NoResultFound, UnmappedInstanceError
from sqlalchemy.exc import OperationalError, DataError, IntegrityError, SQLAlchemyError

from pipeline.config import Config
from pipeline import db
from pipeline.db import Permission
from pipeline.db.processed_file import COMPLETE
from pipeline.db.questions.external_dashboard_queries.utils import (
    get_date_range,
    apply_warehouse_filter,
    _set_athletes_count,
    apply_warehouse_filter_athletes,
)

from pipeline.utils import (
    sort_by_date_for_score,
    sort_by_date_for_all,
    find_shift,
    get_athlete_id_visibility,
)
from pipeline import date_time_utils as dtu
from pipeline.db import Activity
from flask import abort
import boto3
import pyexcel as pe
from athlete_import import init_validation_csv, start_process, valid_columns, get_errors
import io
import sys, os, csv
from werkzeug.utils import secure_filename

# Number of athletes to return for high/low risk list on overview page.
OVERVIEW_ATHLETE_COUNT = 5

logger = logging.getLogger("external_dashboard_queries")
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def get_athlete_query(
    client_id=None,
    athlete_id=None,
    range_start=None,
    range_end=None,
    warehouse_id=None,
    athletes=None,
    csv_query=False,
):
    query = db.db.session.query(
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
        db.Warehouse.prefered_timezone,
        db.IndustrialAthlete.id.label("id"),
        db.IndustrialAthlete.athlete_identifier.label("athlete_identifier"),
        db.IndustrialAthlete.name.label("name"),
        db.IndustrialAthlete.gender.label("gender"),
        db.IndustrialAthlete.hire_date.label("hire_date"),
        db.IndustrialAthlete.db_modified_at.label("last_modified_date"),
        db.Fuse.device_id.label("device_id"),
        db.Fuse.has_flx.label("has_flx"),
        db.ProcessedFile.num_minutes.label("num_minutes"),
    )

    if csv_query:
        query = query.add_columns(
            db.Shifts.name.label("shift"),
            db.JobFunction.name.label("job"),
            db.Warehouse.name.label("facility"),
            db.Warehouse.id.label("warehouse_id"),
            db.Warehouse.prefered_timezone.label("prefered_timezone"),
        )

    query = query.add_columns(
        dtu.convert_tz(
            db.ProcessedFile.start_time, db.UTC_TIMEZONE, db.Warehouse.prefered_timezone
        ).label("start_time"),
        dtu.convert_tz(
            db.ProcessedFile.end_time, db.UTC_TIMEZONE, db.Warehouse.prefered_timezone
        ).label("end_time"),
    )

    query = query.join(
        db.ProcessedFile,
        db.Fuse,
        db.IndustrialAthlete,
        db.Warehouse,
        db.Client,
    )

    if csv_query:
        query = query.join(
            db.JobFunction, db.JobFunction.id == db.IndustrialAthlete.job_function_id
        ).join(db.Shifts, db.Shifts.id == db.IndustrialAthlete.shift_id)

    query = query.filter(
        db.ProcessedFile.version == Config.ALGO_VERSION,
        db.ProcessedFile.status == COMPLETE,
    )

    query = apply_warehouse_filter(query, warehouse_id)

    if client_id:
        query = query.filter(db.Client.id == client_id)

    if athletes:
        query = query.filter(db.IndustrialAthlete.id.in_(athletes))
    if range_start and range_end:
        query = query.filter(
            sa.func.DATE(
                sa.func.CONVERT_TZ(
                    db.ProcessedFile.start_time,
                    db.UTC_TIMEZONE,
                    db.Warehouse.prefered_timezone,
                )
            ).between(range_start, range_end)
        )

    query = query.group_by(
        db.IndustrialAthlete.id, db.ProcessedFile.id, db.Fuse.has_flx
    )

    query = query.order_by("name", "day")

    return query


def get_all_athletes_scores(query, range_start, range_end):
    data = {}
    for row in query:
        if row.day not in data:
            data[row.day] = {
                "id": row.id,
                "name": row.name,
                "athletes": _set_athletes_count(row.id),
                "total_rows": 1,
                "safety_score": row.safety_score,
                "max_flexion": row.max_flexion,
                "avg_twist_velocity": row.avg_twist_velocity,
                "num_minutes": float(row.num_minutes),
                "max_moment": row.max_moment,
                "max_lateral_velocity": row.max_lateral_velocity,
                "lift_rate": row.lift_rate,
                "day": row.day,
            }
        else:
            data[row.day]["id"] = row.id
            data[row.day]["name"] = row.name
            data[row.day]["athletes"].add(row.id)
            data[row.day]["total_rows"] += 1
            data[row.day]["safety_score"] += row.safety_score
            data[row.day]["max_flexion"] += row.max_flexion
            data[row.day]["avg_twist_velocity"] += row.avg_twist_velocity
            data[row.day]["max_moment"] += row.max_moment
            data[row.day]["max_lateral_velocity"] += row.max_lateral_velocity
            data[row.day]["lift_rate"] += row.lift_rate
            data[row.day]["num_minutes"] += float(row.num_minutes)
            data[row.day]["day"] = row.day

    athletes_by_id = []
    for k, athlete in data.items():
        athletes_by_id.append(
            {
                "shift": "All",
                "job_function": "All",
                "day": str(athlete["day"]),
                "safety_score": str(
                    round(
                        athlete["safety_score"] / athlete["total_rows"], Config.ROUNDING
                    )
                ),
                "avg_twist_velocity": str(
                    round(
                        athlete["avg_twist_velocity"] / athlete["total_rows"],
                        Config.ROUNDING,
                    )
                ),
                "max_flexion": str(
                    round(
                        athlete["max_flexion"] / athlete["total_rows"], Config.ROUNDING
                    )
                ),
                "max_moment": str(
                    round(
                        athlete["max_moment"] / athlete["total_rows"], Config.ROUNDING
                    )
                ),
                "max_lateral_velocity": str(
                    round(
                        athlete["max_lateral_velocity"] / athlete["total_rows"],
                        Config.ROUNDING,
                    )
                ),
                "lift_rate": str(
                    round(athlete["lift_rate"] / athlete["total_rows"], Config.ROUNDING)
                ),
                "num_minutes": athlete["num_minutes"],
                "athlete_count": len(athlete["athletes"]),
            }
        )
    return athletes_by_id


def _calculate_score(field, last_score=None, current_score=None):
    last_hour = round(last_score["num_minutes"] / 60.0, 2)
    cur_hour = round(current_score["num_minutes"] / 60.0, 2)
    first_score = last_score[field] * (
        round(last_hour / (last_hour + cur_hour), Config.ROUNDING)
    )
    second_score = current_score[field] * (
        round(cur_hour / (cur_hour + last_hour), Config.ROUNDING)
    )

    return round(first_score + second_score, Config.ROUNDING)


def all_athletes_data_shifts(
    client_id, range_start=None, range_end=None, warehouse_id=None, athlete_ids=None
):
    shifts = (
        db.db.session.query(db.Shifts)
        .join(db.Warehouse)
        .filter(db.Warehouse.client_id == client_id)
        .all()
    )
    range_start, range_end = get_date_range(client_id, range_start, range_end)

    query = get_athlete_query(
        client_id=client_id,
        range_start=range_start,
        range_end=range_end,
        warehouse_id=warehouse_id,
        athletes=athlete_ids,
    )

    data = [row for row in query]

    return data, shifts, range_start, range_end


def individual_athletes_data(
    client_id, range_start=None, range_end=None, warehouse_id=None, athlete_ids=None
):
    data, shifts, range_start, range_end = all_athletes_data_shifts(
        client_id, range_start, range_end, warehouse_id, athlete_ids
    )

    athlete_details_query = (
        db.db.session.query(db.IndustrialAthlete)
        .options(
            joinedload(db.IndustrialAthlete.job_function),
            joinedload(db.IndustrialAthlete.shift),
        )
        .join(db.Client, db.IndustrialAthlete.client_id == db.Client.id)
        .join(db.Warehouse, db.IndustrialAthlete.warehouse_id == db.Warehouse.id)
        .filter(db.Client.id == client_id)
    )

    if athlete_ids and len(athlete_ids) > 0:
        athlete_details_query = athlete_details_query.filter(
            db.IndustrialAthlete.id.in_(athlete_ids)
        )

    athlete_details_query = apply_warehouse_filter(athlete_details_query, warehouse_id)
    athlete_details_query = athlete_details_query.all()

    athlete_details = {
        athlete_detail.id: {
            "id": athlete_detail.id,
            "name": athlete_detail.name,
            "gender": athlete_detail.gender,
            "last_modified_date": athlete_detail.db_modified_at,
            "warehouse": get_rel_name(athlete_detail.warehouse),
            "shift": get_rel_name(athlete_detail.shift),
            "job_function": get_rel_name(athlete_detail.job_function),
            "hire_date": athlete_detail.hire_date,
        }
        for athlete_detail in athlete_details_query
    }

    athletes_by_id = {}
    for athlete in data:
        default = {
            "id": athlete.id,
            "name": athlete.name,
            "gender": str(athlete.gender),
            "hire_date": athlete.hire_date.strftime("%Y-%m-%d")
            if athlete.hire_date
            else None,
            "last_modified_date": athlete.last_modified_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if athlete.hire_date
            else None,
            "warehouse": athlete_details.get(athlete.id, {}).get("warehouse"),
            "shift": athlete_details.get(athlete.id, {}).get("shift"),
            "job_function": athlete_details.get(athlete.id, {}).get("job_function"),
            "scores": [],
            "last_score": {},
        }

        athlete_value = {
            "day": str(athlete.day),
            "safety_score": round(athlete.safety_score, Config.ROUNDING),
            "avg_twist_velocity": round(athlete.avg_twist_velocity, Config.ROUNDING),
            "max_flexion": round(athlete.max_flexion, Config.ROUNDING),
            "max_moment": round(athlete.max_moment, Config.ROUNDING),
            "max_lateral_velocity": round(
                athlete.max_lateral_velocity, Config.ROUNDING
            ),
            "lift_rate": round(athlete.lift_rate, Config.ROUNDING),
            "shift": find_shift(shifts, athlete, athlete.start_time),
            "num_minutes": float(athlete.num_minutes),
        }
        scores = athletes_by_id.setdefault(athlete.id, default)["scores"]
        last_score = None

        if len(scores) > 0:
            last_score = scores[-1]

        if last_score and last_score["day"] == athlete_value["day"]:
            last_score = scores.pop()
            athlete_value["safety_score"] = _calculate_score(
                "safety_score", last_score, athlete_value
            )
            athlete_value["max_moment"] = _calculate_score(
                "max_moment", last_score, athlete_value
            )
            athlete_value["max_flexion"] = _calculate_score(
                "max_flexion", last_score, athlete_value
            )
            athlete_value["avg_twist_velocity"] = _calculate_score(
                "avg_twist_velocity", last_score, athlete_value
            )
            athlete_value["max_lateral_velocity"] = _calculate_score(
                "max_lateral_velocity", last_score, athlete_value
            )
            athlete_value["lift_rate"] = _calculate_score(
                "lift_rate", last_score, athlete_value
            )
            athlete_value["num_minutes"] += last_score["num_minutes"]

        athletes_by_id.setdefault(athlete.id, default)["scores"].append(athlete_value)

    # Add the athlete record if there are no score for a athlete.
    for athlete_id, athlete in athlete_details.iteritems():
        athletes_by_id.setdefault(
            athlete_id,
            athletes_by_id.get(
                athlete_id,
                {
                    "id": athlete["id"],
                    "name": athlete["name"],
                    "hire_date": athlete["hire_date"].strftime("%Y-%m-%d")
                    if athlete["hire_date"]
                    else None,
                    "last_modified_date": athlete["last_modified_date"].strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "gender": str(athlete["gender"]),
                    "warehouse": athlete["warehouse"],
                    "shift": athlete["shift"],
                    "job_function": athlete["job_function"],
                    "last_score": {},
                    "scores": [],
                    "campaigns": athlete["campaigns"],
                },
            ),
        )

    sort_by_date_for_score(athletes_by_id)

    return range_start, range_end, data, athletes_by_id


def individual_date(
    client_id, range_start=None, range_end=None, warehouse_id=None, athlete_ids=None
):
    data, shifts, range_start, range_end = all_athletes_data_shifts(
        client_id, range_start, range_end, warehouse_id, athlete_ids
    )

    athlete_details_query = db.db.session.query(
        db.IndustrialAthlete.id, db.IndustrialAthlete.name
    ).filter(db.Client.id == client_id)

    if athlete_ids and len(athlete_ids) > 0:
        athlete_details_query = athlete_details_query.filter(
            db.IndustrialAthlete.id.in_(athlete_ids)
        )

    athlete_details_query = apply_warehouse_filter(athlete_details_query, warehouse_id)
    athlete_details_query = athlete_details_query.all()

    athlete_details = {
        athlete_detail.id: {"id": athlete_detail.id, "name": athlete_detail.name}
        for athlete_detail in athlete_details_query
    }

    athletes_by_id = {}
    for athlete in data:
        default = {"id": athlete.id, "name": athlete.name, "dates": []}
        athletes_by_id.setdefault(athlete.id, default)["dates"].append(str(athlete.day))

    # Add the athlete record if there are no score for a athlete.
    for athlete_id, athlete in athlete_details.iteritems():
        athletes_by_id.setdefault(
            athlete_id,
            athletes_by_id.get(
                athlete_id,
                {
                    "id": athlete["id"],
                    "name": athlete["name"],
                    "dates": [],
                },
            ),
        )

    for _, athlete in athletes_by_id.items():
        athlete["dates"].sort(
            key=lambda date: datetime.datetime.strptime(date, "%Y-%m-%d").date()
        )

    list = []
    for _, athlete in athletes_by_id.items():
        list.append(athlete)

    return list


def individual_athletes(
    client_id, range_start=None, range_end=None, warehouse_id=None, athlete_ids=None
):
    range_start, range_end, __, athletes_by_id = individual_athletes_data(
        client_id, range_start, range_end, warehouse_id, athlete_ids
    )

    return {"individual_athletes": athletes_by_id}


def all_athletes(
    client_id, range_start=None, range_end=None, warehouse_id=None, athlete_ids=None
):
    data, __, range_start, range_end = all_athletes_data_shifts(
        client_id, range_start, range_end, warehouse_id, athlete_ids
    )

    all_athletes = get_all_athletes_scores(data, range_start, range_end)
    sort_by_date_for_all(all_athletes)
    return {"all_athletes": all_athletes}


def athletes(
    client_id, range_start=None, range_end=None, warehouse_id=None, athlete_ids=None
):
    range_start, range_end, data, athletes_by_id = individual_athletes_data(
        client_id, range_start, range_end, warehouse_id, athlete_ids
    )

    all_athletes = get_all_athletes_scores(data, range_start, range_end)
    sort_by_date_for_all(all_athletes)

    return {"all_athletes": all_athletes, "individual_athletes": athletes_by_id}


def list_athletes(
    client_guid,
    query_str=None,
    is_active=None,
    hire_date_filter=None,
    job_function_filter=None,
    shift_filter=None,
    group_filter=None,
    sort_by=None,
    sort_dir=None,
    offset=None,
    limit=None,
    warehouse_id=None,
):
    query = (
        db.db.session.query(db.IndustrialAthlete)
        .options(
            joinedload(db.IndustrialAthlete.job_function),
            joinedload(db.IndustrialAthlete.shift),
        )
        .join(
            db.Client,
        )
        .filter(db.Client.guid == client_guid)
    )
    query = apply_warehouse_filter(query, warehouse_id)
    query = apply_athletes_list_filters(
        query,
        query_str,
        is_active,
        hire_date_filter,
        job_function_filter,
        shift_filter,
        group_filter,
    )

    if (
        sort_by is not None
        and sort_dir is not None
        and sort_by != ""
        and sort_dir != ""
    ):
        if sort_by == "shift_id":
            query = query.join(
                db.Shifts, db.Shifts.id == db.IndustrialAthlete.shift_id
            ).order_by("shifts.name" + " " + sort_dir)
        elif sort_by == "job_function_id":
            query = query.join(
                db.JobFunction,
                db.JobFunction.id == db.IndustrialAthlete.job_function_id,
            ).order_by("job_function.name" + " " + sort_dir)
        else:
            query = query.order_by("industrial_athlete." + sort_by + " " + sort_dir)

    if offset is not None and limit is not None:
        query = query.offset(offset).limit(limit)

    data = [row for row in query]

    athletes = []

    for row in data:
        athlete = {
            "id": row.id,
            "external_id": row.external_id,
            "name": row.name,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "gender": row.gender,
            "available": row.available,
            "has_haptic": row.has_haptic,
        }

        if row.hire_date is not None:
            athlete["hire_date"] = row.hire_date.strftime("%m-%d-%Y")

        if row.shift is not None:
            athlete["shift"] = row.shift.name

        if row.job_function is not None:
            athlete["job_function"] = row.job_function.name

        athletes.append(athlete)

    count = count_athletes(
        client_guid,
        query_str,
        is_active,
        hire_date_filter,
        job_function_filter,
        shift_filter,
        group_filter,
        warehouse_id,
    )

    result = {"total": count, "rows": athletes}

    return result


def count_athletes(
    client_guid,
    query_str=None,
    is_active=None,
    hire_date_filter=None,
    job_function_filter=None,
    shift_filter=None,
    group_filter=None,
    warehouse_id=None,
):
    query = (
        db.db.session.query(sa.func.count("*"))
        .select_from(db.IndustrialAthlete)
        .join(
            db.Client,
        )
        .filter(db.Client.guid == client_guid)
    )
    query = apply_warehouse_filter(query, warehouse_id)
    query = apply_athletes_list_filters(
        query,
        query_str,
        is_active,
        hire_date_filter,
        job_function_filter,
        shift_filter,
        group_filter,
    )

    return query.scalar()


def apply_athletes_list_filters(
    query,
    query_str=None,
    is_active=None,
    hire_date_filter=None,
    job_function_filter=None,
    shift_filter=None,
    group_filter=None,
):
    if query_str is not None and query_str != "":
        query = query.filter(
            sa.or_(
                db.IndustrialAthlete.external_id.like("%" + query_str + "%"),
                db.IndustrialAthlete.name.like("%" + query_str + "%"),
                db.IndustrialAthlete.first_name.like("%" + query_str + "%"),
                db.IndustrialAthlete.last_name.like("%" + query_str + "%"),
            )
        )

    if is_active is not None:
        query = query.filter(db.IndustrialAthlete.available.is_(is_active))

    if hire_date_filter is not None:
        date = datetime.datetime.now()

        if hire_date_filter == "Last month":
            date = date - datetime.timedelta(days=30)
        elif hire_date_filter == "Last 3 months":
            date = date - datetime.timedelta(days=90)
        elif hire_date_filter == "Last 6 months":
            date = date - datetime.timedelta(days=180)
        elif hire_date_filter == "Last year":
            date = date - datetime.timedelta(days=365)

        query = query.filter(db.IndustrialAthlete.hire_date > date)

    if job_function_filter is not None and job_function_filter != "":
        query = query.join(
            db.JobFunction, db.JobFunction.id == db.IndustrialAthlete.job_function_id
        ).filter(db.JobFunction.name.in_(job_function_filter.split(",")))

    if shift_filter is not None and shift_filter != "":
        query = query.join(
            db.Shifts, db.Shifts.id == db.IndustrialAthlete.shift_id
        ).filter(db.Shifts.name.in_(shift_filter.split(",")))

    return query


def group_count(client_guid, warehouse_id, query_str=None):

    shift_query = """select shifts.name from shifts 
        join warehouse ON warehouse.id = shifts.warehouse_id
        join client ON client.id = warehouse.client_id where client.guid=:clientid"""

    if warehouse_id is not None:
        shift_query = shift_query + " and shifts.warehouse_id=:warehouseId"

    if query_str is not None and query_str != "":
        shift_query += " and shifts.name like :query_str"

    job_function_query = """union 
        select job_function.name from job_function
        join warehouse ON warehouse.id = job_function.warehouse_id
        join client ON client.id = warehouse.client_id where client.guid=:clientid"""

    if warehouse_id is not None:
        job_function_query = (
            job_function_query + " and job_function.warehouse_id=:warehouseId"
        )

    if query_str is not None and query_str != "":
        job_function_query += " and job_function.name like :query_str"

    group_query = """union
        select  athlete_group.name from athlete_group
        join warehouse ON warehouse.id = athlete_group.warehouse_id
        join client ON client.id = warehouse.client_id where client.guid=:clientid"""

    if query_str is not None and query_str != "":
        group_query += " and athlete_group.name like :query_str"

    if query_str is not None and query_str != "":
        group_query += " and athlete_group.name like :query_str"

    unionlist = text(
        "select  count(*) from ("
        + shift_query
        + " "
        + job_function_query
        + " "
        + group_query
        + ") as temp"
    )

    params = dict()

    params["clientid"] = client_guid
    params["warehouseId"] = warehouse_id

    if query_str is not None and query_str != "":
        params["query_str"] = "%" + query_str + "%"
    else:
        params["query_str"] = ""

    query = db.db.session.execute(unionlist, params=params)

    return query.scalar()


def count_group_athletes(groupid, type, warehouse_id):
    if type == "job_function":
        query = db.db.session.query(sa.func.count("*")).select_from(
            db.IndustrialAthlete
        )
        query = query.filter(db.IndustrialAthlete.job_function_id == groupid)
        query = query.filter(db.IndustrialAthlete.available.is_(True))
        query = apply_warehouse_filter(query, warehouse_id)

        return query.scalar()
    if type == "shift":
        query = db.db.session.query(sa.func.count("*")).select_from(
            db.IndustrialAthlete
        )
        query = query.filter(db.IndustrialAthlete.shift_id == groupid)
        query = query.filter(db.IndustrialAthlete.available.is_(True))
        query = apply_warehouse_filter(query, warehouse_id)

        return query.scalar()


def get_shift(id, warehouse_id):
    query = db.db.session.query(db.Shifts).filter(db.Shifts.id == id)
    data = [row for row in query]
    for row in data:
        shift = {
            "id": row.id,
            "name": row.name,
            "shift_start": str(row.shift_start),
            "shift_end": str(row.shift_end),
            "description": row.description,
            "athlete_count": count_group_athletes(row.id, "shift", warehouse_id),
            "group_administrator": row.group_administrator,
            "shift_created_at": str(row.db_created_at.date()),
            "shift_modified_at": str(row.db_modified_at.date()),
            "warehouse": row.warehouse.name,
            "color": row.color,
        }
    return shift


def get_jobfunction(id, warehouse_id):
    query = db.db.session.query(db.JobFunction).filter(db.JobFunction.id == id)
    data = [row for row in query]
    for row in data:
        job = {
            "id": row.id,
            "name": row.name,
            "description": row.description,
            "athlete_count": count_group_athletes(row.id, "job_function", warehouse_id),
            "group_administrator": row.group_administrator,
            "jobfunction_created_at": str(row.db_created_at.date()),
            "jobfunction_modified_at": str(row.db_modified_at.date()),
            "max_package_weight": row.max_package_weight,
            "min_package_weight": row.min_package_weight,
            "avg_package_weight": row.avg_package_weight,
            "lbd_indicence": row.lbd_indicence,
            "lbd_indicence_rate": row.lbd_indicence_rate,
            "warehouse": row.warehouse.name,
            "color": row.color,
        }
    return job


def get_group(id, warehouse_id):
    query = db.db.session.query(db.Group).filter(db.Group.id == id)
    data = [row for row in query]
    for row in data:
        job = {
            "id": row.id,
            "name": row.name,
            "description": row.description,
            "athlete_count": count_group_athletes(
                row.id, "athlete_group", warehouse_id
            ),
            "group_administrator": row.group_administrator,
            "group_created_at": str(row.db_created_at.date()),
            "group_modified_at": str(row.db_modified_at.date()),
            # "warehouse": row.warehouse.name,
            "client": row.client.name,
        }
    return job


def delete_shift(id, warehouse_id):
    if count_group_athletes(id, "shift", warehouse_id) == 0:
        try:
            query = db.db.session.query(db.Shifts).get(id)
            db.db.session.delete(query)
            db.db.session.commit()
            db.db.session.flush()
            return {"message": "Shift Deleted"}
        except UnmappedInstanceError:
            return {"message": "No Shift found with this id"}
    else:
        return {"message": "You can not delete this Shift"}
    return {"message": "Please provide correct data"}


def delete_jobfunction(id, warehouse_id):
    if count_group_athletes(id, "job_function", warehouse_id) == 0:
        try:
            query = db.db.session.query(db.JobFunction).get(id)
            db.db.session.delete(query)
            db.db.session.commit()
            db.db.session.flush()
            return {"message": "Job function Deleted"}
        except UnmappedInstanceError:
            return {"message": "No job function found with this id"}
    else:
        return {"message": "You can not delete this Job function"}
    return {"message": "Please provide correct data"}


def delete_group(id, warehouse_id):
    if count_group_athletes(id, "athlete_group", warehouse_id) == 0:
        try:
            query = db.db.session.query(db.Group).get(id)
            db.db.session.delete(query)
            db.db.session.commit()
            db.db.session.flush()
            return {"message": "Group Deleted"}
        except UnmappedInstanceError:
            return {"message": "No group found with this id"}
    else:
        return {"message": "You can not delete this group"}

    return {"message": "Please provide correct data"}


def get_athlete(client_guid, id):
    query = (
        db.db.session.query(db.IndustrialAthlete)
        .options(
            joinedload(db.IndustrialAthlete.job_function),
            joinedload(db.IndustrialAthlete.shift),
        )
        .join(
            db.Client,
        )
        .filter(db.Client.guid == client_guid)
        .filter(db.IndustrialAthlete.id == id)
    )

    athlete = query.one()
    data = dict()
    data["athlete"] = athlete
    data["campaigns"] = athlete.campaigns
    data["shift"] = athlete.shift
    data["jobFunction"] = athlete.job_function
    return data


def notes(client_guid):
    query = (
        db.db.session.query(db.Note)
        .join(db.Client)
        .filter(db.Client.guid == client_guid)
    )

    result = list()
    for note in query:
        result.append({"id": note.id, "note_text": note.note_text})
    return result


def add_note(request):
    data = json.loads(request.data)
    client_guid = data.get("clientGuid")
    note_text = data.get("noteText")
    if not client_guid or not note_text:
        return {"error": "clientGuid/noteText attributes should have valid values."}
    client = (
        db.db.session.query(db.Client).filter(db.Client.guid == client_guid).first()
    )
    note = db.Note(client=client, note_text=note_text)
    db.db.session.add(note)
    db.db.session.commit()
    return {"id": note.id, "note_text": note.note_text}


def highlights(cid, range_start, range_end, warehouse_id):
    range_start, range_end = get_date_range(cid, range_start, range_end)

    query = get_athlete_query(
        client_id=cid,
        range_start=range_start,
        range_end=range_end,
        warehouse_id=warehouse_id,
    )

    data = [row for row in query]

    athlete_details_query = (
        db.db.session.query(
            db.IndustrialAthlete.id.label("id"), db.IndustrialAthlete.name.label("name")
        )
        .join(db.Client, db.Client.id == db.IndustrialAthlete.client_id)
        .filter(db.Client.id == cid)
    )

    athlete_details_query = apply_warehouse_filter(athlete_details_query, warehouse_id)

    athlete_details = {
        athlete_detail.id: {"id": athlete_detail.id, "name": athlete_detail.name}
        for athlete_detail in athlete_details_query
    }

    athletes_by_id = {}
    for athlete in data:
        default = {
            "id": athlete.id,
            "name": athlete.name,
            "scores": [],
            "last_score": {},
        }

        athlete_value = {
            "day": str(athlete.day),
            "safety_score": str(round(athlete.safety_score, Config.ROUNDING)),
            "avg_twist_velocity": str(
                round(athlete.avg_twist_velocity, Config.ROUNDING)
            ),
            "max_flexion": str(round(athlete.max_flexion, Config.ROUNDING)),
            "max_moment": str(round(athlete.max_moment, Config.ROUNDING)),
            "max_lateral_velocity": str(
                round(athlete.max_lateral_velocity, Config.ROUNDING)
            ),
            "lift_rate": str(round(athlete.lift_rate, Config.ROUNDING)),
        }
        athletes_by_id.setdefault(athlete.id, default)["scores"].append(athlete_value)

    # Add the athlete record if there are no score for a athlete.
    for athlete_id, athlete in athlete_details.iteritems():
        athletes_by_id.setdefault(
            athlete_id,
            athletes_by_id.get(
                athlete_id, {"id": athlete["id"], "name": athlete["name"], "scores": []}
            ),
        )

    list = []
    max_safety = None
    most_days_worn = None
    most_improved_ss = None

    for athlete_id in athletes_by_id:
        list.append(
            athlete_highlight_detail(
                athletes_by_id[athlete_id], athlete_id, range_start, range_end
            )
        )

    list.sort(key=operator.itemgetter("avg_safety"), reverse=True)
    max_safety = copy.deepcopy(list[:5])
    for idx in range(5):
        max_safety[idx]["rank"] = idx + 1

    list.sort(key=operator.itemgetter("most_days_worn"), reverse=True)
    most_days_worn = copy.deepcopy(list[:5])
    for idx in range(5):
        most_days_worn[idx]["rank"] = idx + 1

    list.sort(key=operator.itemgetter("most_improved_ss"), reverse=True)
    most_improved_ss = copy.deepcopy(list[:5])

    for idx in range(5):
        most_improved_ss[idx]["rank"] = idx + 1

    return {
        "highlight": {
            "max_safety": max_safety[:5],
            "most_days_worn": most_days_worn[:5],
            "most_improved_ss": most_improved_ss[:5],
        }
    }


def get_rel_name(relation):
    if not relation:
        return
    return relation.name


def get_campaigns(campaigns):
    camps = []
    for camp in campaigns:
        if not camp.is_archived:
            campaign = {
                "id": camp.id,
                "campaign_type": camp.campaign_type,
                "title": camp.title,
                "start_date": camp.start_date,
                "end_date": camp.end_date,
                "manager_email": camp.manager_email,
                "description": camp.description,
                "color": camp.color,
                "campaign_state": camp.campaign_state,
            }
            camps.append(campaign)
    return camps


def has_group_data_in_table(group_list, table):
    return (
        db.db.session.query(sa.func.count(table.id))
        .filter(sa.func.lower(table.name).in_(group_list))
        .scalar()
        > 0
    )


def join_filter_by_group(data, group_list, table):
    data = data.join(table)
    return data.filter(sa.func.lower(table.name).in_(group_list))


def rankings(cid, range_start, range_end, warehouse_id, group_list=None):
    range_start, range_end = get_date_range(cid, range_start, range_end)
    athletes = []

    query = get_athlete_query(
        client_id=cid,
        range_start=range_start,
        range_end=range_end,
        warehouse_id=warehouse_id,
        athletes=athletes,
    )

    data = [row for row in query]

    athlete_details_query = (
        db.db.session.query(db.IndustrialAthlete)
        .options(
            joinedload(db.IndustrialAthlete.shift),
            joinedload(db.IndustrialAthlete.job_function),
        )
        .filter(db.IndustrialAthlete.client_id == cid)
    )

    if athletes is not None and len(athletes) > 0:
        athlete_details_query = athlete_details_query.filter(
            db.IndustrialAthlete.id.in_(athletes)
        )

    athlete_details_query = apply_warehouse_filter(
        athlete_details_query, warehouse_id
    ).all()
    athlete_details = {}

    show_athlete_identifier, show_athlete_name = get_athlete_id_visibility(cid)
    for athlete_detail in athlete_details_query:
        if athlete_detail.id not in athlete_details:
            athlete_details[athlete_detail.id] = {}

        athlete_details[athlete_detail.id]["id"] = athlete_detail.id
        if show_athlete_identifier:
            athlete_details[athlete_detail.id][
                "athlete_identifier"
            ] = athlete_detail.athlete_identifier
        if show_athlete_name:
            athlete_details[athlete_detail.id]["name"] = athlete_detail.name

        athlete_details[athlete_detail.id]["groups"] = get_group_name_list(
            athlete_detail
        )
        athlete_details[athlete_detail.id]["shift"] = get_rel_name(athlete_detail.shift)
        athlete_details[athlete_detail.id]["job_function"] = get_rel_name(
            athlete_detail.job_function
        )

    athletes_by_id = {}
    for athlete in data:
        default = {
            "id": athlete.id,
            "shift": athlete_details.get(athlete.id, {}).get("shift"),
            "job_function": athlete_details.get(athlete.id, {}).get("job_function"),
            "scores": [],
            "last_score": {},
            "day": str(athlete.day),
        }

        if show_athlete_identifier:
            default["athlete_identifier"] = athlete.athlete_identifier

        if show_athlete_name:
            default["name"] = athlete.name

        athlete_value = {
            "day": str(athlete.day),
            "safety_score": str(round(athlete.safety_score, Config.ROUNDING)),
            "avg_twist_velocity": str(
                round(athlete.avg_twist_velocity, Config.ROUNDING)
            ),
            "max_flexion": str(round(athlete.max_flexion, Config.ROUNDING)),
            "max_moment": str(round(athlete.max_moment, Config.ROUNDING)),
            "max_lateral_velocity": str(
                round(athlete.max_lateral_velocity, Config.ROUNDING)
            ),
            "lift_rate": str(round(athlete.lift_rate, Config.ROUNDING)),
        }
        athletes_by_id.setdefault(athlete.id, default)["scores"].append(athlete_value)

    # Add the athlete record if there are no score for a athlete.
    for athlete_id, athlete in athlete_details.iteritems():
        athletes_by_id.setdefault(
            athlete_id,
            athletes_by_id.get(
                athlete_id,
                {
                    "id": athlete["id"],
                    "shift": athlete["shift"],
                    "job_function": athlete["job_function"],
                    "scores": [],
                },
            ),
        )

        if show_athlete_identifier:
            athletes_by_id[athlete_id]["athlete_identifier"] = athlete[
                "athlete_identifier"
            ]

        if show_athlete_name:
            athletes_by_id[athlete_id]["name"] = athlete["name"]

    list = []
    for athlete_id in athletes_by_id:
        list.append(
            athlete_rank_detail(
                athletes_by_id[athlete_id],
                athlete_id,
                show_athlete_identifier,
                show_athlete_name,
            )
        )

    list.sort(key=operator.itemgetter("avg_safety"), reverse=True)

    for idx, item in enumerate(list):
        list[idx]["rank"] = idx + 1

    return {"individual_athletes": list}


def athlete_highlight_detail(athlete, id, range_start, range_end):
    if not athlete:
        return None

    if not athlete["scores"]:
        return {
            "name": athlete["name"],
            "id": id,
            "avg_safety": 0,
            "most_days_worn": 0,
            "most_improved_ss": 0,
        }

    count = len(athlete["scores"])
    safety_score = 0
    days = 0
    safety_start_date = -1

    athlete["scores"].sort(key=operator.itemgetter("day"))
    for score in athlete["scores"]:
        safety_score += float(score["safety_score"])
        days += 1
        if safety_start_date == -1:
            safety_start_date = float(score["safety_score"])

    avg_safety_score = float(safety_score) / count

    if safety_start_date > 0 and count > 1:
        most_improved_ss = (
            (avg_safety_score - safety_start_date) / float(safety_start_date)
        ) * 100
        most_improved_ss = round(most_improved_ss, Config.ROUNDING)
    else:
        most_improved_ss = -999999

    return {
        "name": athlete["name"],
        "id": id,
        "avg_safety": round((avg_safety_score / 100) * 100, Config.ROUNDING),
        "most_days_worn": days,
        "most_improved_ss": round(most_improved_ss, Config.ROUNDING),
    }


def athlete_rank_detail(athlete, id, show_athlete_identifier, show_athlete_name):
    if not athlete:
        return None

    if not athlete["scores"]:
        data = {
            "id": athlete["id"],
            "avg_safety": 0,
            "avg_safety_perc": "0%",
            "improve": "Lateral Velocity",
            "groups": athlete["groups"],
            "shift": athlete["shift"],
            "job_function": athlete["job_function"],
            "dates": [],
        }

        if show_athlete_identifier:
            data["athlete_identifier"] = athlete["athlete_identifier"]

        if show_athlete_name:
            data["name"] = athlete["name"]

        return data

    count = len(athlete["scores"])
    safety_score = 0
    max_flexion = 0
    max_lateral_velocity = 0
    twist_velocity = 0
    dates = []

    for score in athlete["scores"]:
        safety_score += float(score["safety_score"])
        max_flexion += float(score["max_flexion"])
        max_lateral_velocity += float(score["max_lateral_velocity"])
        twist_velocity += float(score["avg_twist_velocity"])
        dates.append(score["day"])

    avg_safety_score = safety_score / count
    avg_max_flexion = max_flexion / count
    avg_max_lateral_velocity = max_lateral_velocity / count
    avg_twist_velocity = twist_velocity / count
    avg_safety_perc = (avg_safety_score / 100) * 100
    data = {
        "id": athlete["id"],
        "avg_safety": round(avg_safety_score, Config.ROUNDING),
        "avg_safety_perc": "{} %".format(round(avg_safety_score, Config.ROUNDING)),
        "improve": can_improve(
            avg_max_flexion,
            avg_max_lateral_velocity,
            avg_twist_velocity,
            avg_safety_perc,
        ),
        "groups": athlete["groups"],
        "shift": athlete["shift"],
        "job_function": athlete["job_function"],
        "dates": dates,
    }

    if show_athlete_identifier:
        data["athlete_identifier"] = athlete["athlete_identifier"]

    if show_athlete_name:
        data["name"] = athlete["name"]

    return data


def can_improve(max_flexion, max_lateral_velocity, avg_twist_velocity, avg_safety_perc):
    avg_twist_velocity_p = avg_twist_velocity / 40 * 100
    max_lateral_velocity_p = max_lateral_velocity / 110 * 100
    max_flexion_p = max_flexion / 110 * 100
    p = max([avg_twist_velocity_p, max_lateral_velocity_p, max_flexion_p])

    message = "Keep Up the Good Lifting!"
    if p == max_lateral_velocity_p and avg_safety_perc < 75:
        message = "Lateral Velocity"
    elif p == avg_twist_velocity_p and avg_safety_perc < 75:
        message = "Twist Velocity"
    elif p == max_flexion_p and avg_safety_perc < 75:
        message = "Max Flexion"

    return message


def ranking_pdf_data(cid, range_start, range_end, warehouse_id, name, group_list=[]):

    show_athlete_identifier, show_athlete_name = get_athlete_id_visibility(cid)
    data = rankings(cid, range_start, range_end, warehouse_id, group_list=group_list)
    fieldnames = ["rank", "avg_safety_perc", "improve"]
    labels = ["Rank", "Avg Safety Score", "What to Improve"]

    if name and name == "1" or show_athlete_name:
        fieldnames.insert(1, "name")
        labels.insert(1, "Name")

    if show_athlete_identifier:
        fieldnames.insert(1, "athlete_identifier")
        labels.insert(1, "ID")

    res = []
    if data["individual_athletes"]:
        for item in data["individual_athletes"]:
            if item.get("avg_safety_perc", "") != "0%":
                inner_list = []
                for key in fieldnames:
                    if key == "athlete_identifier" and item.get(key, None) is None:
                        inner_list.append("N/A")
                    else:
                        inner_list.append(item.get(key, ""))
                res.append(inner_list)

        res.insert(0, labels)
        return res

    return None


def highlight_pdf_data(cid, range_start, range_end, warehouse_id, name):
    data = highlights(cid, range_start, range_end, warehouse_id)
    field_max_safety = ["rank", "id", "avg_safety"]
    field_most_days_worn = ["rank", "id", "most_days_worn"]
    field_most_improved_ss = ["rank", "id", "most_improved_ss"]
    label_field_max_safety = ["Rank", "ID", "Avg Safety Score"]
    label_field_most_days_worn = ["Rank", "ID", "Most Days Worn"]
    label_field_most_improved_ss = ["Rank", "ID", "Most Improved Score"]

    if name and name == "1":
        field_max_safety = ["rank", "name", "id", "avg_safety"]
        field_most_days_worn = ["rank", "name", "id", "most_days_worn"]
        field_most_improved_ss = ["rank", "name", "id", "most_improved_ss"]
        label_field_max_safety = ["Rank", "Name", "ID", "Avg Safety Score"]
        label_field_most_days_worn = ["Rank", "Name", "ID", "Most Days Worn"]
        label_field_most_improved_ss = ["Rank", "Name", "ID", "Most Improved Score"]

    res = {}
    if data["highlight"]:
        res["max_safety"] = get_highlight_table(
            data["highlight"]["max_safety"],
            label_field_max_safety,
            field_max_safety,
            "avg_safety",
            is_percent=1,
        )

        res["most_days_worn"] = get_highlight_table(
            data["highlight"]["most_days_worn"],
            label_field_most_days_worn,
            field_most_days_worn,
            "most_days_worn",
            is_percent=0,
        )

        res["most_improved_ss"] = get_highlight_table(
            data["highlight"]["most_improved_ss"],
            label_field_most_improved_ss,
            field_most_improved_ss,
            "most_improved_ss",
            is_percent=1,
        )
        return res

    return None


def get_highlight_table(data, labels, fieldnames, data_key, is_percent=0):
    res = []
    for item in data:
        if item.get(data_key, 0) != 0:
            if is_percent:
                res.append(
                    [
                        "{} %".format(item.get(key, 0))
                        if key == data_key
                        else item.get(key, "")
                        for key in fieldnames
                    ]
                )
            else:
                res.append(
                    [
                        item.get(key, 0) if key == data_key else item.get(key, "")
                        for key in fieldnames
                    ]
                )

    res.insert(0, labels)
    return res


def export_athletes_csv(cid, range_start, range_end, warehouse_id, athletes=None):
    client = db.db.session.query(db.Client).filter(db.Client.id == cid).scalar()
    shifts = (
        db.db.session.query(db.Shifts)
        .join(db.Warehouse)
        .filter(db.Warehouse.client_id == cid)
        .all()
    )
    range_start, range_end = get_date_range(cid, range_start, range_end)
    data = []

    query = get_athlete_query(
        client_id=cid,
        range_start=range_start,
        range_end=range_end,
        warehouse_id=warehouse_id,
        athletes=athletes,
        csv_query=True,
    )
    data.append(
        [
            "Name",
            "Facility",
            "Hire Date",
            "Job Function",
            "Shift",
            "Date",
            "Avg. Safety Score",
            "Avg. Max Flexion",
            "Avg Twist Velocity",
            "Max Moment",
            "Max Lateral Velocity",
            "Lift Rate",
            "Hours of Valid Lift Data",
            "Start Time",
            "End Time",
            "Timezone",
        ]
    )

    for athlete in query:
        shift = athlete.shift

        if client.dynamic_shift:
            shift = find_shift(shifts, athlete, athlete.start_time)

        record = [
            athlete.name,
            athlete.facility,
            athlete.hire_date,
            athlete.job,
            shift,
            athlete.day,
            round(athlete.safety_score, Config.ROUNDING),
            round(athlete.max_flexion, Config.ROUNDING),
            round(athlete.avg_twist_velocity, Config.ROUNDING),
            round(athlete.max_moment, Config.ROUNDING),
            round(athlete.max_lateral_velocity, Config.ROUNDING),
            round(athlete.lift_rate, Config.ROUNDING),
            round(athlete.num_minutes / 60, Config.ROUNDING),
            athlete.start_time,
            athlete.end_time,
            athlete.prefered_timezone,
        ]
        data.append(record)

    return data


def groups_athletes_csv(group_id, group_name):
    query = db.db.session.query(db.IndustrialAthlete)
    if group_name == "shift":
        query = query.filter(db.IndustrialAthlete.shift_id == group_id)
    elif group_name == "job_function":
        query = query.filter(db.IndustrialAthlete.job_function_id == group_id)
    elif group_name == "athlete_group":
        query = query.join(
            db.groups, db.IndustrialAthlete.id == db.groups.c.industrial_athlete_id
        ).filter(db.groups.c.group_id == group_id)
    data = []
    data.append(
        [
            "Id",
            "Name",
            "First Name",
            "Last Name",
            "Gender",
            "Shift",
            "Job Function",
            "External ID",
            "Hire Date",
            "weight",
            "height",
            "Schedule",
            "Warehouse",
            "Client",
            "Status",
            "Has Haptic",
            "Athlete identifier",
            "Db Create at",
            "Db Modified at",
        ]
    )

    for athlete in query:
        shift = None
        jobfunction = None
        if athlete.shift.name is not None or athlete.shift.name != "":
            shift = athlete.shift.name
        if athlete.job_function.name is not None or athlete.job_function.name != "":
            jobfunction = athlete.job_function.name
        record = [
            athlete.id,
            athlete.name,
            athlete.first_name,
            athlete.last_name,
            athlete.gender,
            shift,
            jobfunction,
            athlete.external_id,
            athlete.hire_date,
            athlete.weight,
            athlete.height,
            athlete.schedule,
            athlete.warehouse.name,
            athlete.client.name,
            athlete.available,
            athlete.has_haptic,
            athlete.athlete_identifier,
            str(athlete.db_created_at),
            str(athlete.db_modified_at),
        ]
        data.append(record)

    return data


def deactivate_athletes(filterdata):
    try:
        query = db.db.session.query(db.IndustrialAthlete)
        query = apply_action_filters(query, filterdata)

        query.update({"available": 0}, synchronize_session="fetch")
        db.db.session.commit()
        db.db.session.flush()
        return {"message": "Athletes deactivated successfully"}
    except NoResultFound:
        return {"message": "No athlete found with this filter criteria"}
    return {"message": "Please provide correct data"}


def activate_athletes(filterdata):
    try:
        query = db.db.session.query(db.IndustrialAthlete)
        query = apply_action_filters(query, filterdata)

        query.update({"available": 1}, synchronize_session="fetch")
        db.db.session.commit()
        db.db.session.flush()
        return {"message": "Athletes Updated succesffuly "}
    except NoResultFound:
        return {"message": "No athlete found with this filter critera"}
    return {"message": "Please provide correct data"}


def update_athletes_job_function(filterdata):
    try:
        query = db.db.session.query(db.IndustrialAthlete)
        query = apply_action_filters(query, filterdata)

        query.update(
            {"job_function_id": filterdata["job_function_id"]},
            synchronize_session="fetch",
        )
        db.db.session.commit()
        db.db.session.flush()
        if "includeIds" in filterdata and len(filterdata["includeIds"]) > 0:
            athletes_ids = filterdata["includeIds"]
            res = trigger_reprocessing_api(athletes_ids)
            if res:
                status = "UPDATED"
            else:
                status = "UPDATED BUT REPOCESS FILE FAILED"

        return {"message": "Athletes Updated succesffuly ", "status": status}
    except NoResultFound:
        return {"message": "No athlete found with this filter critera"}
    return {"message": "Please provide correct data"}


def update_athletes_shift(filterdata):
    try:
        query = db.db.session.query(db.IndustrialAthlete)
        query = apply_action_filters(query, filterdata)

        query.update({"shift_id": filterdata["shift_id"]}, synchronize_session="fetch")
        db.db.session.commit()
        db.db.session.flush()
        return {"message": "Athletes Updated succesffuly "}
    except NoResultFound:
        return {"message": "No athlete found with this filter critera"}
    return {"message": "Please provide correct data"}


def update_athletes_groups(filterdata):
    try:
        query = db.db.session.query(db.IndustrialAthlete)
        query = apply_action_filters(query, filterdata)

        for athlete in query:
            if "groupAdds" in filterdata and filterdata["groupAdds"] is not None:
                for groupId in filterdata["groupAdds"]:
                    Group = db.db.session.query(db.Group).get(groupId)
                    if Group and Group is not None:
                        Group.athletes.append(athlete)
                db.db.session.commit()

            if "groupRemoves" in filterdata and filterdata["groupRemoves"] is not None:
                for groupId in filterdata["groupRemoves"]:
                    Group = db.db.session.query(db.Group).get(groupId)
                    if Group and Group is not None:
                        for searchedAthlete in Group.athletes:
                            if athlete.id == searchedAthlete.id:
                                Group.athletes.remove(searchedAthlete)
                db.db.session.commit()

        return {"message": "Athletes activated succesffuly "}
    except NoResultFound:
        return {"message": "No athlete found with this filter critera"}
    return {"message": "Please provide correct data"}


def apply_action_filters(query, filterdata):
    if (
        "jobFunctionFilter" in filterdata
        and filterdata["jobFunctionFilter"] is not None
        and len(filterdata["jobFunctionFilter"]) > 0
    ):
        query = query.filter(
            db.IndustrialAthlete.job_function_id.in_(filterdata["jobFunctionFilter"])
        )

    if (
        "shiftFilter" in filterdata
        and filterdata["shiftFilter"] is not None
        and len(filterdata["shiftFilter"]) > 0
    ):
        query = query.filter(
            db.IndustrialAthlete.shift_id.in_(filterdata["shiftFilter"])
        )

    if (
        "customGroupFilter" in filterdata
        and filterdata["customGroupFilter"] is not None
        and len(filterdata["customGroupFilter"]) > 0
    ):
        query = query.filter(db.groups.c.group_id.in_(filterdata["customGroupFilter"]))

    if "includeIds" in filterdata and len(filterdata["includeIds"]) > 0:
        query = query.filter(db.IndustrialAthlete.id.in_(filterdata["includeIds"]))

    if "excludeIds" in filterdata and len(filterdata["excludeIds"]) > 0:
        query = query.filter(~db.IndustrialAthlete.id.in_(filterdata["excludeIds"]))

    return query


def check_duplicate_group(warehouse_id, name):
    shifts_query = (
        db.db.session.query(db.Shifts.name)
        .filter(db.Shifts.warehouse_id == warehouse_id)
        .filter(db.Shifts.name == name)
    )
    jobfunction_query = (
        db.db.session.query(db.JobFunction.name)
        .filter(db.JobFunction.warehouse_id == warehouse_id)
        .filter(db.JobFunction.name == name)
    )
    athlete_group_query = (
        db.db.session.query(db.Group.name)
        .filter(db.Group.warehouse_id == warehouse_id)
        .filter(db.Group.name == name)
    )
    query = shifts_query.union(jobfunction_query, athlete_group_query).all()
    # data = [row for row in query]
    if query:
        return True
    else:
        return False


def create_shifts(request, user_id, client_id, warehouse_id):
    data = json.loads(request.data)
    if not data:
        return {"message": "No input data provided"}
    if check_duplicate_group(warehouse_id, data.get("name")):
        return {"message": "A group already exists with same name"}
    shift = db.Shifts(
        name=data.get("name"),
        group_administrator=data.get("group_administrator"),
        description=data.get("description"),
        warehouse_id=warehouse_id,
    )
    if (
        "shift_start" in data
        and data["shift_start"] is not None
        and data["shift_start"] != ""
    ):
        start_shift = datetime.datetime.strptime(
            data.get("shift_start"), "%H:%M:%S"
        ).time()
        shift.shift_start = start_shift
    else:
        shift.shift_start = datetime.datetime.now()

    if (
        "shift_end" in data
        and data["shift_end"] is not None
        and data["shift_end"] != ""
    ):
        end_shift = datetime.datetime.strptime(data.get("shift_end"), "%H:%M:%S").time()
        shift.shift_end = end_shift
    else:
        shift.shift_end = datetime.datetime.now()

    try:
        db.db.session.add(shift)
        db.db.session.commit()
        db.db.session.flush()

        Activity.save_activity(user_id, client_id, "shifts", shift.id, "CREATED")

        return {"success": True, "id": shift.id}

    except SQLAlchemyError as e:
        return {"success": False, "error": e.message}

    except OperationalError as e:
        return {"success": False, "error": e.message}

    except DataError as e:
        return {"success": False, "error": e.message}

    except IntegrityError as e:
        return {"success": False, "error": e.message}


def create_job_functions(request, user_id, client_id, warehouse_id):
    data = json.loads(request.data)
    if not data:
        return {"message": "No input data provided"}
    if check_duplicate_group(warehouse_id, data.get("name")):
        return {"message": "A group already exists with same name"}
    job_function = db.JobFunction(
        name=data.get("name"),
        group_administrator=data.get("group_administrator"),
        max_package_weight=data.get("max_package_weight"),
        min_package_weight=data.get("min_package_weight"),
        avg_package_weight=data.get("avg_package_weight"),
        lbd_indicence=data.get("lbd_indicence"),
        lbd_indicence_rate=data.get("lbd_indicence_rate"),
        description=data.get("description"),
        warehouse_id=warehouse_id,
    )
    try:
        db.db.session.add(job_function)
        db.db.session.commit()
        db.db.session.flush()

        Activity.save_activity(
            user_id, client_id, "job_function", job_function.id, "CREATED"
        )

        return {"success": True, "id": job_function.id}

    except SQLAlchemyError as e:
        return {"success": False, "error": e.message}

    except OperationalError as e:
        return {"success": False, "error": e.message}

    except DataError as e:
        return {"success": False, "error": e.message}

    except IntegrityError as e:
        return {"success": False, "error": e.message}


def create_athlete(request, user_id, client_id, warehouse_id):
    data = json.loads(request.data)
    if not data:
        return {"message": "No input data provided"}
    exists = (
        db.db.session.query(db.IndustrialAthlete.external_id)
        .filter(db.IndustrialAthlete.client_id == client_id)
        .filter(db.IndustrialAthlete.external_id == data.get("external_id"))
        .first()
    )
    if exists:
        return {"message": "Duplicate entry for customer id"}
    schedule = None
    if data.get("schedule") and data.get("schedule") is not None:
        schedule = ",".join(data.get("schedule"))

    athlete = db.IndustrialAthlete(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        name=data.get("first_name") + " " + data.get("last_name"),
        gender=data.get("gender").lower(),
        height=data.get("height"),
        weight=data.get("weight"),
        hire_date=datetime.datetime.strptime(data.get("hire_date"), "%m-%d-%Y")
        if data.get("hire_date")
        else None,
        external_id=data.get("external_id"),
        job_function_id=data.get("job_function_id"),
        shift_id=data.get("shift_id"),
        prior_back_injuries=data.get("prior_back_injuries"),
        warehouse_id=warehouse_id,
        available=1,
        has_haptic=False,
        client_id=client_id,
        schedule=schedule,
    )
    try:
        db.db.session.add(athlete)
        db.db.session.commit()
        if data.get("groups"):
            for group in data.get("groups"):
                Group = db.db.session.query(db.Group).get(group)
                if Group and Group is not None:
                    Group.athletes.append(athlete)
            db.db.session.commit()

        Activity.save_activity(
            user_id, client_id, "industrial_athlete", athlete.id, "CREATED"
        )

        return {"success": True}

    except OperationalError as e:
        return {"success": False, "error": e.message}

    except DataError as e:
        return {"success": False, "error": e.message}

    except IntegrityError as e:
        return {"success": False, "error": e.message}


def update_athlete(id, request, user_id, client_id, warehouse_id):
    data = json.loads(request.data)
    schedule = None
    if data.get("schedule") and data.get("schedule") is not None:
        schedule = ",".join(data.get("schedule"))
    if not data:
        return {"message": "No input data provided"}
    try:
        athlete = (
            db.db.session.query(db.IndustrialAthlete)
            .filter(db.IndustrialAthlete.id == id)
            .first()
        )

        athlete.first_name = data.get("first_name")
        athlete.last_name = data.get("last_name")
        athlete.name = data.get("first_name") + " " + data.get("last_name")
        athlete.gender = data.get("gender").lower()
        athlete.height = data.get("height")
        athlete.weight = data.get("weight")
        athlete.hire_date = (
            datetime.datetime.strptime(data.get("hire_date"), "%m-%d-%Y")
            if data.get("hire_date")
            else None,
        )
        athlete.external_id = data.get("external_id")
        athlete.job_function_id = data.get("job_function_id")
        athlete.shift_id = data.get("shift_id")
        athlete.prior_back_injuries = data.get("prior_back_injuries")
        athlete.has_haptic = data.get("has_haptic")
        athlete.schedule = schedule
        db.db.session.merge(athlete)
        db.db.session.commit()

        # adding new records
        if data.get("groups"):
            for group in data.get("groups"):
                Group = db.db.session.query(db.Group).get(group)
                if Group and Group is not None:
                    Group.athletes.append(athlete)
            db.db.session.commit()

        Activity.save_activity(
            user_id, client_id, "industrial_athlete", athlete.id, "UPDATED"
        )

        return {"success": True}

    except SQLAlchemyError as e:
        return {"success": False, "error": e.message}
    except OperationalError as e:
        return {"success": False, "error": e.message}
    except DataError as e:
        return {"success": False, "error": e.message}


def update_group(id, request, user_id, client_id, warehouse_id):
    data = json.loads(request.data)
    if not data:
        return {"message": "No input data provided"}
    try:
        group = db.db.session.query(db.Group).filter(db.Group.id == id).first()
        group.name = data.get("name")
        group.group_administrator = data.get("group_administrator")
        group.description = data.get("description")
        db.db.session.merge(group)
        db.db.session.commit()
        db.db.session.flush()

        Activity.save_activity(user_id, client_id, "athlete_group", group.id, "UPDATED")

        return {"success": True}
    except SQLAlchemyError as e:
        return {"success": False, "error": e.message}

    except OperationalError as e:
        return {"success": False, "error": e.message}

    except DataError as e:
        return {"success": False, "error": e.message}

    except IntegrityError as e:
        return {"success": False, "error": e.message}


def reprocess_on_athlete_change(job_func_id, user_id, client_id, athletes):
    if athletes and len(athletes) > 0:
        res = trigger_reprocessing_api(athletes)
        if res:
            status = "UPDATED"
        else:
            status = "UPDATED BUT REPOCESS FILE FAILED"
        Activity.save_activity(user_id, client_id, "job_function", job_func_id, status)


def update_jobfunction(id, request, user_id, client_id, warehouse_id):
    data = json.loads(request.data)
    if not data:
        return {"message": "No input data provided"}

    jobfunction = (
        db.db.session.query(db.JobFunction).filter(db.JobFunction.id == id).first()
    )
    jobfunction.name = data.get("name")
    jobfunction.group_administrator = data.get("group_administrator")
    jobfunction.description = data.get("description")
    jobfunction.max_package_weight = data.get("max_package_weight")
    jobfunction.min_package_weight = data.get("min_package_weight")
    jobfunction.avg_package_weight = data.get("avg_package_weight")
    jobfunction.lbd_indicence = data.get("lbd_indicence")
    jobfunction.lbd_indicence_rate = data.get("lbd_indicence_rate")
    try:
        db.db.session.merge(jobfunction)
        db.db.session.commit()
        db.db.session.flush()
        query = db.db.session.query(db.IndustrialAthlete.id).filter(
            db.IndustrialAthlete.job_function_id == job_func_id
        )
        data = [row for row in query]
        athletes = []
        for row in data:
            athletes.append(row.id)
        reprocess_on_athlete_change(jobfunction.id, user_id, client_id, athletes)
        return {"success": True}
    except SQLAlchemyError as e:
        return {"success": False, "error": e.message}

    except OperationalError as e:
        return {"success": False, "error": e.message}

    except DataError as e:
        return {"success": False, "error": e.message}

    except IntegrityError as e:
        return {"success": False, "error": e.message}


def update_shift(id, request, user_id, client_id, warehouse_id):
    data = json.loads(request.data)
    schedule = None
    if not data:
        return {"message": "No input data provided"}

    shift = db.db.session.query(db.Shifts).filter(db.Shifts.id == id).first()
    shift.name = data.get("name")
    shift.group_administrator = data.get("group_administrator")
    shift.description = data.get("description")
    if (
        "shift_start" in data
        and data["shift_start"] is not None
        and data["shift_start"] != ""
    ):
        start_shift = datetime.datetime.strptime(
            data.get("shift_start"), "%H:%M:%S"
        ).time()
        shift.shift_start = start_shift
    else:
        shift.shift_start = datetime.datetime.now()

    if (
        "shift_end" in data
        and data["shift_end"] is not None
        and data["shift_end"] != ""
    ):
        end_shift = datetime.datetime.strptime(data.get("shift_end"), "%H:%M:%S").time()
        shift.shift_end = end_shift
    else:
        shift.shift_end = datetime.datetime.now()
    try:
        db.db.session.merge(shift)
        db.db.session.commit()
        db.db.session.flush()

        Activity.save_activity(user_id, client_id, "shifts", shift.id, "UPDATED")

        return {"success": True}
    except SQLAlchemyError as e:
        return {"success": False, "error": e.message}

    except OperationalError as e:
        return {"success": False, "error": e.message}

    except DataError as e:
        return {"success": False, "error": e.message}

    except IntegrityError as e:
        return {"success": False, "error": e.message}


def upload_file(request, client_id, user_id, s3_bucket, s3_location):
    if not request:
        return {"message": "No input data provided"}
    if request.method == "POST" and request.files["file"] != "":
        file_name = (
            str(datetime.datetime.now().time()) + "-" + request.files["file"].filename
        )
        total_records = sum(1 for row in request.files["file"]) - 1
        location = upload_to_s3(request, file_name, s3_bucket, s3_location)
        importrecord = ImportRecord(
            filename=file_name, user_id=user_id, location=location
        )
        try:
            db.db.session.add(importrecord)
            db.db.session.commit()
            db.db.session.flush()
            Activity.save_activity(
                user_id, client_id, "import_record", importrecord.id, "CREATED"
            )
            return {
                "success": True,
                "importId": importrecord.id,
                "total_records": total_records,
            }
        except SQLAlchemyError as e:
            return {"success": False, "error": e.message}

        except OperationalError as e:
            return {"success": False, "error": e.message}

        except DataError as e:
            return {"success": False, "error": e.message}

        except IntegrityError as e:
            return {"success": False, "error": e.message}
    else:
        return {"success": False, "error": "Please select a file to upload"}


def upload_to_s3(request, file_name, bucket_name, bucket_location):
    session = boto3.Session(
        aws_access_key_id="AKIAJCOTAHRIMHSF6GYA",
        aws_secret_access_key="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",
        region_name="us-east-1",
    )
    s3 = session.resource("s3")
    try:
        content = request.files["file"].getvalue()
        s3.Bucket(bucket_name).put_object(Key=file_name, Body=content)
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        return e
    return "{}{}".format(bucket_location, file_name)


def process_file(id, client_id, warehouse_id, user_id, s3_bucket, s3_location):
    import_record = (
        db.db.session.query(ImportRecord).filter(ImportRecord.id == id).first()
    )

    error, total_records, inserted_records = start_process(
        import_record.location,
        import_record.filename,
        s3_bucket,
        client_id,
        warehouse_id,
        id,
        user_id,
    )
    import_errors = []
    if error > 0:
        import_errors = get_errors(id)
        return {
            "rows_with_error": error,
            "total_records": total_records,
            "errors": import_errors,
        }

    return {"total_records": total_records, "inserted_records": inserted_records}


def import_status(id):

    query_athlete = db.db.session.query(sa.func.count("*")).select_from(
        db.IndustrialAthlete
    )
    query_athlete = query_athlete.filter(db.IndustrialAthlete.import_record_id == id)
    total_insert = query_athlete.scalar()

    query = text(
        """ SELECT count(distinct row_number) from import_error where import_record_id=:id """
    )
    query_error = db.db.session.execute(query, params=dict(id=id)).scalar()

    total = total_insert + query_error
    if query_athlete or query_error:
        return {
            "success": True,
            "total_process": total,
            "error": query_error,
            "insert": total_insert,
        }
    else:
        return {"success": False}


def download_bulk_upload_csv_format():
    data = []
    Note = "Note: Job Functions and Shifts must match titles created in the dashboard. Use the legend below to populate the data for Job Functions and Shifts"
    data.append(
        [
            "*First Name",
            "*Last Name",
            "*Customer ID",
            "*Gender (M/F/Other)",
            "Weight (lbs)",
            "Height (in)",
            "*Known Prior Back Injuries (Y/N/Do Not Specifiy)",
            "Hire Date (mm/dd/yyyy)",
            "*Job Function",
            "*Shift",
            "",
            Note,
        ]
    )
    data.append(["", "", "", "", "", "", "", "", "", "", "", "", ""])
    data.append(["", "", "", "", "", "", "", "", "", "", "", "Legend", ""])
    data.append(["", "", "", "", "", "", "", "", "", "", "", "JobFunction", "Shift"])
    data.append(["", "", "", "", "", "", "", "", "", "", "", "", ""])
    data.append(["", "", "", "", "", "", "", "", "", "", "", "Unload", "AM"])
    data.append(["", "", "", "", "", "", "", "", "", "", "", "Load", "PM"])
    data.append(["", "", "", "", "", "", "", "", "", "", "", "Packing", "Night"])
    data.append(["", "", "", "", "", "", "", "", "", "", "", "Shipping", ""])
    data.append(["", "", "", "", "", "", "", "", "", "", "", "Receiving", ""])
    return data


def trigger_reprocessing_api(athletes):
    athlete_ids = ",".join(str(elm) for elm in athletes)
    try:
        resonse = requests.get(
            "https://x3ird0fstb.execute-api.us-east-1.amazonaws.com/staging/reprocess?athlete_id_list="
            + athlete_ids
            + "&overwrite=true"
        )
        logging.info(resonse.status_code)
        if resonse.status_code == 200:
            return True
        else:
            return False
    except ConnectionError as e:
        logging.info(e)
        return False
    except Timeout as e:
        logging.info(e)
        return False


def update_haptic(id, request):
    data = json.loads(request.data)
    if not data:
        return {"message": "No input data provided"}
    try:
        athlete = (
            db.db.session.query(db.IndustrialAthlete)
            .filter(db.IndustrialAthlete.id == id)
            .first()
        )
        athlete.has_haptic = data.get("has_haptic")
        db.db.session.merge(athlete)
        db.db.session.commit()
        return {"success": True}

    except SQLAlchemyError as e:
        return {"success": False, "error": e.message}
    except OperationalError as e:
        return {"success": False, "error": e.message}
    except DataError as e:
        return {"success": False, "error": e.message}


def get_roles(email):
    user = db.db.session.query(db.User).filter_by(email=email).first()
    roles = user.user_role
    roles_users = []
    for row in roles:
        roles_users.append(row.title)
    return roles_users
