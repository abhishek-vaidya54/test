import math

import sqlalchemy as sa

from pipeline.config import Config
from pipeline import db


def _round_down(num, base=5):
    return base * math.floor(float(num) / base)


def _round_up(num, base=5):
    return base * math.ceil(float(num) / base)


metric_dict = {
    "safety-score": sa.func.avg(db.Risk.safety_score).label("Avg Safety Score"),
    "lift-rate": sa.func.avg(db.Risk.lift_rate).label("Avg Lift Rate"),
    "max-flexion": sa.func.avg(db.Risk.max_flexion).label("Avg Max Flexion"),
    "avg-flexion": sa.func.avg(db.Risk.average_flexion).label("Average Flexion"),
    "max-lateral-velocity": sa.func.avg(db.Risk.max_lateral_velocity).label(
        "Max Lateral Velocity"
    ),
    "avg-twist-velocity": sa.func.avg(db.Risk.avg_twist_velocity).label(
        "Average Twist Velocity"
    ),
}


def get_athlete_query(athlete_ids, metric):
    query = (
        db.db.session.query(
            metric_dict[metric],
            sa.func.avg(db.Risk.max_lateral_velocity).label("FilterMLV"),
            sa.func.DATE(db.Risk.start_time).label("day"),
            db.Fuse.has_flx.label("has_flx"),
            db.IndustrialAthlete.id.label("id"),
            db.IndustrialAthlete.name.label("name"),
        )
        .join(
            db.ProcessedFile,
            db.Fuse,
            db.IndustrialAthlete,
            db.Warehouse,
            db.Client,
        )
        .filter(db.ProcessedFile.version == Config.ALGO_VERSION)
        .filter(db.IndustrialAthlete.id.in_(athlete_ids if athlete_ids else []))
        .group_by(
            db.IndustrialAthlete.id,
            db.IndustrialAthlete.name,
            db.Fuse.has_flx,
            sa.func.DATE(db.Risk.start_time),
        )
    )

    return query


def athlete_average_by_rel_day(athlete_ids, metric="safety-score"):
    assert metric in metric_dict

    query = get_athlete_query(athlete_ids, metric)
    data = {}
    for athlete in query:
        athlete_data = data.setdefault(
            athlete.id,
            {"flx": [], "no_flx": [], "name": athlete.name, "athlete_id": athlete.id},
        )
        key = "flx" if athlete.has_flx else "no_flx"
        athlete_data[key].append(float(athlete[0]))
    return data
