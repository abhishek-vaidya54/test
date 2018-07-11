import datetime

from pipeline import db
import sqlalchemy as sa
from pipeline.config import Config
from pipeline import date_time_utils as dtu
from pipeline.server.constant_data import MINIMUM_DAYS_TO_INTERVENTION, CAMPAIGN_COLOR_CHOICES
from pipeline.utils import sort_by_date_for_all, sort_by_date_for_score
from datetime import timedelta
from flask import request, jsonify
from pipeline.server.schemas import CampaignSchema, CampaignSchemaLimited
from marshmallow.exceptions import ValidationError
from sqlalchemy.sql.expression import false, true



def sort_by_date_for_all(all_athletes_scores):
    all_athletes_scores.sort(
        key=lambda score: datetime.datetime.strptime(
            score['day'], "%Y-%m-%d").date())

def sort_by_days(all_athletes_scores):
    all_athletes_scores.sort(
        key=lambda score: score["day"]
    )

def remove_old_campaigns(athletes, warehouse_id=None, campaign_id=None):
    for athlete in athletes:
        old_campaigns = db.db.session.query(db.Campaign).join(db.Campaign.athletes).filter(
            db.IndustrialAthlete.id == athlete.id
        )
        if campaign_id:
            old_campaigns = old_campaigns.filter(db.Campaign.id != campaign_id)

        for campaign in old_campaigns:
            campaign.athletes.remove(athlete)
            if len(campaign.athletes) == 0:
                db.db.session.delete(campaign)

            db.db.session.commit()

        athlete.db_modified_at = datetime.datetime.utcnow()
        db.db.session.commit()
        db.db.session.flush()


def create_campaign(warehouse_id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    try:
        data, errors = CampaignSchema().load(json_data)
    except ValidationError as exp:
        data, errors = None, exp.message
    if errors:
        return jsonify(errors), 422
    athletes = []
    if 'athletes' in data:
        athletes = data.pop('athletes')

    if athletes:
        athlete_ids = [athlete['id'] for athlete in athletes]

        athletes = db.db.session.query(db.IndustrialAthlete).filter(
            db.IndustrialAthlete.id.in_(athlete_ids),
            db.IndustrialAthlete.warehouse_id == warehouse_id
        )
        athletes = [athlete for athlete in athletes]
        data['athletes'] = athletes
        remove_old_campaigns(athletes, warehouse_id=warehouse_id)

    data['warehouse_id'] = warehouse_id
    campaign = db.Campaign(**data)

    db.db.session.add(campaign)
    db.db.session.commit()
    db.db.session.flush()

    schema = CampaignSchema()
    campaign, _ = schema.dump(campaign)

    return jsonify(campaign)

def get_athlete_campaigns(athlete_id, warehouse_id):
    query = db.db.session.query(
        db.Campaign.id,
        db.Campaign.campaign_type,
        db.Campaign.title,
        db.Campaign.start_date,
        db.Campaign.end_date,
        db.Campaign.manager_email,
        db.Campaign.description,
        db.Campaign.color,
        db.Campaign.campaign_state
    ).filter(
        db.Campaign.warehouse_id == warehouse_id,
        db.Campaign.is_archived == false(),
        db.Campaign.athletes.any(id=athlete_id)
    )

    schema = CampaignSchema()
    campaigns, _ = schema.dump(query, many=True)

    return campaigns


def campaigns_list(warehouse_id):
    query = db.db.session.query(db.Campaign).filter(db.Campaign.warehouse_id == warehouse_id)

    schema = CampaignSchema()
    campaigns, _ = schema.dump(query, many=True)

    return campaigns


def campaign_detail_simple(warehouse_id, campaign_id):
    campaign = db.db.session.query(db.Campaign).filter(
        db.Campaign.warehouse_id == warehouse_id,
        db.Campaign.id == campaign_id).first()
    if not campaign:
        return jsonify({"message": "The campaign not found"}), 404

    campaign_json, _ = CampaignSchema().dump(campaign)

    return jsonify(campaign_json)


def update_campaign_details(warehouse_id, campaign_id):
    campaign = db.db.session.query(db.Campaign).filter(
        db.Campaign.warehouse_id == warehouse_id,
        db.Campaign.id == campaign_id).first()
    if not campaign:
        return jsonify({"message": "The campaign not found"}), 404
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    campaign_scheme = CampaignSchema()
    try:
        errors = campaign_scheme.validate(json_data)
    except ValidationError as exp:
        errors = exp.message
    if errors:
        return jsonify(errors), 422
    try:
        data, errors = campaign_scheme.load(json_data)
    except ValidationError as exp:
        data, errors = None, exp.message
    if errors:
        return jsonify(errors), 422

    athletes = []
    if "athletes" in data:
        athletes = data.pop("athletes")
    campaign_type = data.get("campaign_type")
    color = data.get("color")

    if color not in dict(CAMPAIGN_COLOR_CHOICES).keys():
        return jsonify({'message': 'invalid color'}), 400

    if campaign_type not in ["baseline", "intervention"]:
        return jsonify({'message': 'invalid campaign type'}), 400

    if athletes:
        athlete_ids = [athlete['id'] for athlete in athletes]
        athletes = db.db.session.query(db.IndustrialAthlete).filter(
            db.IndustrialAthlete.id.in_(athlete_ids)).filter(
            db.IndustrialAthlete.warehouse_id == warehouse_id)

        athletes = [athlete for athlete in athletes]
        remove_old_campaigns(
            athletes,
            warehouse_id=warehouse_id,
            campaign_id=campaign_id
        )

    for key, value in data.items():
        setattr(campaign, key, value)

    campaign.db_modified_at = datetime.datetime.utcnow()
    db.db.session.add(campaign)
    campaign.athletes = list(athletes)

    db.db.session.commit()
    db.db.session.flush()

    end_date = campaign.end_date
    today = datetime.datetime.utcnow().date()

    if end_date > today:
        end_date = today - datetime.timedelta(days=1)

    kwargs = {
        "start_date": campaign.start_date,
        "end_date": end_date,
        "athletes": campaign.athletes or [],
        "display_type": "dates",
        "client_guid": None,
        "warehouse_id": warehouse_id
    }

    data = avg(progress(**kwargs), len(campaign.athletes) or 0)
    campaign, _ = campaign_scheme.dump(campaign)
    campaign["average"] = data

    return jsonify(campaign)


def delete_campaign(warehouse_id, campaign_id):
    campaign = db.db.session.query(db.Campaign).filter(
        db.Campaign.warehouse_id == warehouse_id,
        db.Campaign.id == campaign_id).first()
    if not campaign:
        return jsonify({"message": "The campaign not found"}), 404
    db.db.session.delete(campaign)
    db.db.session.commit()

    return jsonify({"message": "The campaign deleted."}), 200


def get_shifts(warehouse_id):
    if not warehouse_id:
        return {'status': "Pease enter valid warehouse id", 'code': 404}

    query = db.db.session.query(db.Shifts).filter(
        db.Shifts.warehouse_id == warehouse_id
    )

    shifts = []
    for shift in query:
        shifts.append({
            'id': shift.id,
            'name': shift.name,
            'shift_start': shift.shift_start.strftime("%H:%M"),
            'shift_end': shift.shift_end.strftime("%H:%M")
        })

    return shifts


def get_job_function(warehouse_id):
    if not warehouse_id:
        return {'status': "Pease enter valid warehouse id", 'code': 404}

    query = db.db.session.query(db.JobFunction).filter(
        db.JobFunction.warehouse_id == warehouse_id
    )

    job_functions = []
    for job_function in query:
        job_functions.append({
            'id': job_function.id,
            'name': job_function.name,
            'max_package_mass': job_function.max_package_mass
        })

    return job_functions


def archived_campaign(campaign_id):
    if not campaign_id:
        return {'status': "Pease enter valid campaign id", 'code': 404}

    campaign = db.db.session.query(db.Campaign).filter(
        db.Campaign.id==campaign_id
    ).update({ "campaign_state": db.Campaign.DRAFT })
    db.db.session.commit()
    db.db.session.flush()

    return {'status': "Campaign Number# " + campaign_id + " updated to archived", 'code': 200}


def active_campaign(campaign_id):
    if not campaign_id:
        return {'status': "Pease enter valid campaign id", 'code': 404}

    campaign = db.db.session.query(db.Campaign).filter(
        db.Campaign.id==campaign_id
    ).update({ "campaign_state": db.Campaign.ACTIVE })
    db.db.session.commit()
    db.db.session.flush()

    return {'status': "Campaign Number# " + campaign_id + " updated to active", 'code': 200}


def get_athlete_query(athlete_ids, range_start=None, range_end=None):
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
        db.IndustrialAthlete.id.label('id'),
        db.IndustrialAthlete.name.label('name'),
        db.IndustrialAthlete.gender.label('gender'),
        db.ProcessedFile.num_minutes.label('num_minutes')
    ).join(
        db.ProcessedFile,
        db.Fuse,
        db.IndustrialAthlete,
    ).join(
        db.Client, db.Client.id == db.IndustrialAthlete.client_id
    ).join(
        db.Warehouse, db.Warehouse.id == db.IndustrialAthlete.warehouse_id
    ).filter(
        db.ProcessedFile.version == Config.ALGO_VERSION
    ).filter(
        sa.func.DATE(
            dtu.convert_tz(
                db.ProcessedFile.start_time,
                db.UTC_TIMEZONE,
                db.Warehouse.prefered_timezone)) >= range_start,
        sa.func.DATE(
            dtu.convert_tz(
                db.ProcessedFile.start_time,
                db.UTC_TIMEZONE,
                db.Warehouse.prefered_timezone)) <= range_end
    )

    if athlete_ids and len(athlete_ids) > 0:
        query = query.filter(
            db.IndustrialAthlete.id.in_(athlete_ids)
        )
    return query


def _set_athletes_count(aid):
    athletes = set()
    athletes.add(aid)
    return athletes


def get_min_days_to_intervention():
    return MINIMUM_DAYS_TO_INTERVENTION


def get_intervention_start_date(campaign):
    intervention_start_date = campaign.start + timedelta(days=get_min_days_to_intervention())
    return intervention_start_date


def get_all_athletes_scores(query, range_start, range_end):
    data = {}
    for row in query:
        if row.day not in data:
            data[row.day] = {
                'id': row.id,
                'name': row.name,
                'athletes': _set_athletes_count(row.id),
                'total_rows': 1,
                'safety_score': row.safety_score,
                'max_flexion': row.max_flexion,
                'avg_twist_velocity': row.avg_twist_velocity,
                'num_minutes': row.num_minutes,
                'max_moment': row.max_moment,
                'max_lateral_velocity': row.max_lateral_velocity,
                'lift_rate': row.lift_rate,
                'day': row.day
            }
        else:
            data[row.day]['id'] = row.id
            data[row.day]['name'] = row.name
            data[row.day]['athletes'].add(row.id)
            data[row.day]['total_rows'] += 1
            data[row.day]['safety_score'] += row.safety_score
            data[row.day]['max_flexion'] += row.max_flexion
            data[row.day]['avg_twist_velocity'] += row.avg_twist_velocity
            data[row.day]['max_moment'] += row.max_moment
            data[row.day]['max_lateral_velocity'] += row.max_lateral_velocity
            data[row.day]['lift_rate'] += row.lift_rate
            data[row.day]['num_minutes'] += row.num_minutes
            data[row.day]['day'] = row.day

    athletes_by_id = []
    for k, athlete in data.items():
        athletes_by_id.append(
            {"shift": "All", "job_function": "All", "day": str(athlete['day']),
             "safety_score": str(round(athlete['safety_score'] / athlete['total_rows'], Config.ROUNDING)),
             "avg_twist_velocity": str(
                 round(athlete['avg_twist_velocity'] / athlete['total_rows'], Config.ROUNDING)
             ),
             "max_flexion": str(round(athlete['max_flexion'] / athlete['total_rows'], Config.ROUNDING)),
             "max_moment": str(round(athlete['max_moment'] / athlete['total_rows'], Config.ROUNDING)),
             "max_lateral_velocity": str(
                 round(athlete['max_lateral_velocity'] / athlete['total_rows'], Config.ROUNDING)
             ),
             "lift_rate": str(
                 round(athlete['lift_rate'] / athlete['total_rows'], Config.ROUNDING)
             ),
             "num_minutes": float(athlete['num_minutes']),
             "athlete_count": len(athlete['athletes'])
             })
    return athletes_by_id

def get_all_athletes_safty_scores(query):
    data = {}
    for row in query:
        if row.day not in data:
            data[row.day] = {
                'id': row.id,
                'total_rows': 1,
                'safety_score': row.safety_score,
                'day': row.day
            }
        else:
            data[row.day]['id'] = row.id
            data[row.day]['total_rows'] += 1
            data[row.day]['safety_score'] += row.safety_score
            data[row.day]['day'] = row.day

    athletes_by_id = []
    for k, athlete in data.items():
        athletes_by_id.append({
            "shift": "All",
            "job_function": "All",
            "day": str(athlete['day']),
            "safety_score": str(round(athlete['safety_score'] / athlete['total_rows'], Config.ROUNDING)),
        })
    return athletes_by_id

def get_all_athletes_scores_by_days(query, range_start, range_end):
    athletes_by_id = get_all_athletes_scores(query, range_start, range_end)
    scores = []
    day = 1
    for score in athletes_by_id:
        if score["athlete_count"] == 0:
            continue

        score["day"] = day
        scores.append(score)
        day += 1

    return scores


def baseline_campaign(campaign_id, range_start, range_end):
    result = {}
    campaign = db.db.session.query(db.Campaign).filter(db.Campaign.id == campaign_id).first()
    if campaign:
        athlete_ids = [athlete.id for athlete in campaign.athletes]
        query = get_athlete_query(athlete_ids, range_start=range_start, range_end=range_end)
        query = query.group_by(
            db.IndustrialAthlete.id,
            sa.func.DATE(
                dtu.convert_tz(
                    db.Risk.start_time,
                    db.UTC_TIMEZONE,
                    db.Warehouse.prefered_timezone
                )
            )
        ).order_by('name', 'day')
        data = [row for row in query]

        athlete_details_query = db.db.session.query(
            db.IndustrialAthlete.id.label('id'),
            db.IndustrialAthlete.name.label('name'),
            db.IndustrialAthlete.gender.label('gender'),
            db.Warehouse.name.label('warehouse'),
            db.Shifts.name.label('shift'),
            db.JobFunction.name.label('job_function')
        ).join(
            db.Client, db.Client.id == db.IndustrialAthlete.client_id
        ).outerjoin(
            db.Warehouse, db.IndustrialAthlete.warehouse_id == db.Warehouse.id
        ).outerjoin(
            db.JobFunction,
            db.IndustrialAthlete.job_function_id == db.JobFunction.id
        ).outerjoin(
            db.Shifts, db.IndustrialAthlete.shift_id == db.Shifts.id
        ).filter(db.IndustrialAthlete.id.in_(athlete_ids))

        athlete_details = {
            athlete_detail.id: {
                "id": athlete_detail.id,
                "name": athlete_detail.name,
                "gender": athlete_detail.gender,
                "warehouse": athlete_detail.warehouse,
                "shift": athlete_detail.shift,
                "job_function": athlete_detail.job_function
            } for athlete_detail in athlete_details_query
        }

        athletes_by_id = {}
        for athlete in data:
            athletes_by_id.setdefault(
                athlete.id,
                {
                    "id": athlete.id, "name": athlete.name,
                    "gender": str(athlete.gender),
                    "warehouse": athlete_details.get(athlete.id, {}).get(
                        "warehouse"
                    ),
                    "shift": athlete_details.get(athlete.id, {}).get("shift"),
                    "job_function": athlete_details.get(athlete.id, {}).get(
                         "job_function"
                    ),
                    "scores": [],
                    "last_score": {},
                })["scores"].append({
                    "day": str(athlete.day),
                    "safety_score": str(round(athlete.safety_score, Config.ROUNDING)),
                    "avg_twist_velocity": str(
                        round(athlete.avg_twist_velocity, Config.ROUNDING)
                    ),
                    "max_flexion": str(round(athlete.max_flexion, Config.ROUNDING)),
                    "max_moment": str(round(athlete.max_moment, Config.ROUNDING)),
                    "max_lateral_velocity": str(round(athlete.max_lateral_velocity, Config.ROUNDING)),
                    "lift_rate": str(round(athlete.lift_rate, Config.ROUNDING)),
                    "num_minutes": athlete.num_minutes
                })

        # Add the athlete record if there are no score for a athlete.
        for athlete_id, athlete in athlete_details.iteritems():
            athletes_by_id.setdefault(
                athlete_id,
                athletes_by_id.get(
                    athlete_id,
                    {
                        "id": athlete["id"],
                        "name": athlete["name"],
                        "gender": str(athlete["gender"]),
                        "warehouse": athlete["warehouse"],
                        "shift": athlete["shift"],
                        "job_function": athlete["job_function"],
                        "last_score": {},
                        "scores": []
                    }
                )
            )

        all_athletes = get_all_athletes_scores(
            data, range_start, range_end
        )

        sort_by_date_for_all(all_athletes)
        sort_by_date_for_score(athletes_by_id)

        result = {
            "id": campaign.id,
            "title": campaign.title,
            "start": campaign.start,
            "campaign_purpose_id": campaign.campaign_purpose_id,
            "campaign_problem_id": campaign.campaign_problem_id,
            "manager_email": campaign.manager_email,
            "goals": campaign.goals,
            "campaign_state": campaign.campaign_state,
            "minimum_days_to_intervention": get_min_days_to_intervention(),
            "intervention_start": get_intervention_start_date(campaign),
            "all_athletes": all_athletes,
            "individual_athletes": athletes_by_id
        }
    return result


def campaigns_with_score(warehouse_id, active_or_archived):
    if active_or_archived == 'archived':
        is_archived = true()
    else:
        is_archived = false()
    def get_safety_score_query(athlete_ids, range_start=None, range_end=None):
        query = db.db.session.query(
            sa.func.avg(db.Risk.safety_score).label('safety_score'),
            sa.func.DATE(
                dtu.convert_tz(
                    db.ProcessedFile.start_time,
                    db.UTC_TIMEZONE,
                    db.Warehouse.prefered_timezone
                )
            ).label('day'),
            db.Fuse.athlete_id.label('id'),
        ).join(
            db.ProcessedFile,
            db.Fuse,
        ).filter(
            db.ProcessedFile.version == Config.ALGO_VERSION
        ).filter(
            sa.func.DATE(
                dtu.convert_tz(
                    db.ProcessedFile.start_time,
                    db.UTC_TIMEZONE,
                    db.Warehouse.prefered_timezone)) >= range_start,
            sa.func.DATE(
                dtu.convert_tz(
                    db.ProcessedFile.start_time,
                    db.UTC_TIMEZONE,
                    db.Warehouse.prefered_timezone)) <= range_end
        )

        if athlete_ids and len(athlete_ids) > 0:
            query = query.filter(
                db.Fuse.athlete_id.in_(athlete_ids)
            )
        return query

    campaigns = db.db.session.query(
        db.Campaign
    ).filter(
        db.Campaign.is_archived == is_archived,
        db.Campaign.warehouse_id == warehouse_id
    ).order_by('db_modified_at')

    campaign_details = []
    for campaign in campaigns:
        schema = CampaignSchema()
        campaign_overview, _ = schema.dump(campaign)
        athlete_ids = [a.id for a in campaign.athletes]

        query = get_safety_score_query(
            athlete_ids=athlete_ids,
            range_start=campaign.start_date,
            range_end=campaign.end_date,
        )
        query = query.filter(
            db.Warehouse.id == warehouse_id
        )
        query = query.group_by(
            db.Fuse.athlete_id,
            db.ProcessedFile.id,
            db.Fuse.has_flx
        ).order_by('name', 'day')
        data = [row for row in query]

        all_athletes = get_all_athletes_safty_scores(data)

        count = len(all_athletes) or 1
        safety_score = 0

        for score in all_athletes:
            safety_score += float(score["safety_score"])

        score = {
            "avg_safety_score": round(float(safety_score) / count, Config.ROUNDING)
        }

        campaign_overview["safety_score"] = score["avg_safety_score"]
        campaign_overview["total_athletes"] = len(campaign.athletes)

        campaign_details.append(campaign_overview)

    return campaign_details


def campaigns_detail(client_id, warehouse_id, payload=None):
    """Get detail of multiple campaigns"""
    if not client_id or not warehouse_id or not payload:
        return {
            "message": "please enter valid data"
        }

    display_type = "dates"
    start_date = None
    end_date = None

    if "display" in payload:
        display_type = payload["display"]

    if "start" in payload:
        try:
            start_date = int(payload["start"])
        except ValueError:
            start_date = datetime.datetime.strptime(payload["start"] , '%Y-%m-%d')

    if "end" in payload:
        try:
            end_date = int(payload["end"])
        except ValueError:
            end_date = datetime.datetime.strptime(payload["end"], '%Y-%m-%d')

    client_guid = db.db.session.query(db.Client.guid).filter(db.Client.id == client_id).scalar()
    campaign_details = {}

    for campaign_obj in payload["campaigns"]:
        data = {}
        campaign_query = db.db.session.query(db.Campaign).filter(
            db.Campaign.warehouse_id == warehouse_id,
            db.Campaign.id == campaign_obj["id"]
        ).first()

        # overview of campaign
        schema = CampaignSchemaLimited()
        data["overview"], _ = schema.dump(campaign_query)

        # calculate progress
        if campaign_query:
            _start_date = None
            _end_date = None
            if start_date is None or not isinstance(start_date, datetime.date):
                _start_date = campaign_query.start_date
            else:
                _start_date = start_date.date()

            if end_date is None or not isinstance(end_date, datetime.date):
                _end_date = campaign_query.end_date
            else:
                _end_date = end_date.date()

            today = datetime.datetime.utcnow().date()
            athletes_count = len(campaign_query.athletes)
            print athletes_count, campaign_query.athletes

            if _end_date > today:
                _end_date = today - datetime.timedelta(days=1)

            kwargs = {
                "start_date": _start_date,
                "end_date": _end_date,
                "start_day": start_date,
                "end_day": end_date,
                "athletes": campaign_query.athletes or [],
                "display_type": display_type,
                "client_guid": client_guid,
                "warehouse_id": warehouse_id
            }
            data["progress"] = progress(**kwargs)
            data["average"] = avg(data["progress"], athletes_count)

            campaign_details[str(campaign_obj["id"])] = data

    return campaign_details

def progress(**kwargs):
    if kwargs.get('display_type', "dates") == "days":
        return progress_by_days(**kwargs)

    return progress_by_dates(**kwargs)

def progress_by_days(**kwargs):
    athlete_ids = [athlete.id for athlete in kwargs.get('athletes', [])]
    query = get_athlete_query(
        athlete_ids=athlete_ids,
        range_start=kwargs.get('start_date'),
        range_end=kwargs.get('end_date')
    )

    if kwargs.get('client_guid'):
        query = query.filter(
            db.Client.guid == kwargs.get('client_guid')
        )

    if kwargs.get('warehouse_id'):
        query = query.filter(
            db.Warehouse.id == kwargs.get('warehouse_id')
        )

    query = query.group_by(
        db.IndustrialAthlete.id,
        db.ProcessedFile.id,
        db.Fuse.has_flx
    ).order_by('name', 'day')
    data = [row for row in query]

    all_athletes = get_all_athletes_scores_by_days(
        data, kwargs.get('start_date'), kwargs.get('end_date')
    )
    sort_by_days(all_athletes)
    count = len(all_athletes)
    start_day = kwargs.get('start_day', 1)
    end_day = kwargs.get('end_day', all_athletes[count - 1]["day"] if count > 0 else -1)
    res = []
    for s in all_athletes:
        if s["day"] < start_day:
            continue
        if s["day"] > end_day:
            break
        res.append(s)

    return res

def progress_by_dates(**kwargs):
    athlete_ids = [ athlete.id for athlete in kwargs.get('athletes', []) ]
    query = get_athlete_query(
        athlete_ids=athlete_ids,
        range_start=kwargs.get('start_date'),
        range_end=kwargs.get('end_date'),
    )
    if kwargs.get('client_guid'):
        query = query.filter(
            db.Client.guid == kwargs.get('client_guid')
        )

    if kwargs.get('warehouse_id'):
        query = query.filter(
            db.Warehouse.id == kwargs.get('warehouse_id')
        )

    query = query.group_by(
        db.IndustrialAthlete.id,
        db.ProcessedFile.id,
        db.Fuse.has_flx
    ).order_by('name', 'day')
    data = [row for row in query]

    all_athletes = get_all_athletes_scores(
        data, kwargs.get('start_date'), kwargs.get('end_date')
    )
    sort_by_date_for_all(all_athletes)
    return all_athletes

def avg(data, athlete_count):
    count = len(data)
    avg_twist_velocity = 0
    lift_rate = 0
    max_flexion = 0
    max_lateral_velocity = 0
    max_moment = 0
    safety_score = 0

    for score in data:
        avg_twist_velocity += float(score["avg_twist_velocity"])
        lift_rate += float(score["lift_rate"])
        max_flexion += float(score["max_flexion"])
        max_lateral_velocity += float(score["max_lateral_velocity"])
        max_moment += float(score["max_moment"])
        safety_score += float(score["safety_score"])

    count = count or 1
    return {
        "athlete_count": athlete_count,
        "avg_twist_velocity": round(avg_twist_velocity/count, Config.ROUNDING),
        "avg_lift_rate": round(lift_rate/count, Config.ROUNDING),
        "avg_max_flexion": round(max_flexion/count, Config.ROUNDING),
        "avg_max_lateral_velocity": round(max_lateral_velocity/count, Config.ROUNDING),
        "avg_max_moment": round(max_moment/count, Config.ROUNDING),
        "avg_safety_score": round(safety_score/count, Config.ROUNDING)
    }


def campaigns_high_risk(client_id, warehouse_id, payload=None):
    """Get detail of multiple campaigns"""
    if not client_id or not warehouse_id or not payload:
        return {
            "message": "please enter valid data"
        }

    client_guid = db.db.session.query(db.Client.guid).filter(db.Client.id == client_id).scalar()
    campaign_details = {}

    display_type = "dates"
    start_date = None
    end_date = None

    if "display" in payload:
        display_type = payload["display"]

    if "start" in payload:
        try:
            start_date = int(payload["start"])
        except ValueError:
            start_date = datetime.datetime.strptime(payload["start"] , '%Y-%m-%d')

    if "end" in payload:
        try:
            end_date = int(payload["end"])
        except ValueError:
            end_date = datetime.datetime.strptime(payload["end"], '%Y-%m-%d')

    for campaign_obj in payload["campaigns"]:
        data = {}
        campaign_query = db.db.session.query(db.Campaign).filter(
            db.Campaign.warehouse_id == warehouse_id,
            db.Campaign.id == campaign_obj["id"]
        ).first()

        # calculate progress
        if campaign_query:
            _start_date = None
            _end_date = None
            if start_date is None or not isinstance(start_date, datetime.date):
                _start_date = campaign_query.start_date
            else:
                _start_date = start_date.date()

            if end_date is None or not isinstance(end_date, datetime.date):
                _end_date = campaign_query.end_date
            else:
                _end_date = end_date.date()

            today = datetime.datetime.utcnow().date()
            athletes_count = len(campaign_query.athletes) or 1

            if _end_date > today:
                _end_date = today - datetime.timedelta(days=1)

            kwargs = {
                "start_date": _start_date,
                "end_date": _end_date,
                "start_day": start_date,
                "end_day": end_date,
                "display_type": display_type,
                "athletes": campaign_query.athletes or [],
                "client_guid": client_guid,
                "warehouse_id": warehouse_id
            }
            data["all_athletes"] = high_risk(**kwargs)
            data["risk_info"] = high_risk_info(data["all_athletes"], athletes_count)
            campaign_details[str(campaign_obj["id"])] = data

    return campaign_details


def high_risk(**kwargs):
    athlete_ids = [athlete.id for athlete in kwargs.get('athletes', [])]
    query = get_athlete_query(
        athlete_ids=athlete_ids,
        range_start=kwargs.get('start_date'),
        range_end=kwargs.get('end_date'),
    )
    query = query.filter(
        db.Client.guid == kwargs.get('client_guid'),
        db.Warehouse.id == kwargs.get('warehouse_id')
    )
    query = query.group_by(
        db.IndustrialAthlete.id,
        db.ProcessedFile.id,
        db.Fuse.has_flx
    ).order_by('name', 'day')
    data = [row for row in query]

    athlete_details_query = db.db.session.query(
        db.IndustrialAthlete.id.label('id'),
        db.IndustrialAthlete.name.label('name'),
        db.IndustrialAthlete.gender.label('gender'),
        db.Warehouse.name.label('warehouse'),
        db.Shifts.name.label('shift'),
        db.JobFunction.name.label('job_function')
    ).join(
        db.Client, db.Client.id == db.IndustrialAthlete.client_id
    ).outerjoin(
        db.Warehouse, db.IndustrialAthlete.warehouse_id == db.Warehouse.id
    ).outerjoin(
        db.JobFunction,
        db.IndustrialAthlete.job_function_id == db.JobFunction.id
    ).outerjoin(
        db.Shifts, db.IndustrialAthlete.shift_id == db.Shifts.id
    ).filter(
        db.Client.guid == kwargs.get('client_guid'),
        db.IndustrialAthlete.id.in_(athlete_ids),
        db.Warehouse.id == kwargs.get('warehouse_id')
    )

    athlete_details = {
        athlete_detail.id: {
            "id": athlete_detail.id,
            "name": athlete_detail.name,
            "gender": athlete_detail.gender,
            "warehouse": athlete_detail.warehouse,
            "shift": athlete_detail.shift,
            "job_function": athlete_detail.job_function
        } for athlete_detail in athlete_details_query
    }

    athletes_by_id = {}
    for athlete in data:
        default = {
            "id": athlete.id,
            "name": athlete.name,
            "gender": str(athlete.gender),
            "warehouse": athlete_details.get(athlete.id, {}).get("warehouse"),
            "shift": athlete_details.get(athlete.id, {}).get("shift"),
            "job_function": athlete_details.get(athlete.id, {}).get("job_function"),
            "scores": []
        }

        athlete_value = {
            "day": str(athlete.day),
            "safety_score": str(round(athlete.safety_score, Config.ROUNDING)),
            "avg_twist_velocity": str(round(athlete.avg_twist_velocity, Config.ROUNDING)),
            "max_flexion": str(round(athlete.max_flexion, Config.ROUNDING)),
            "max_moment": str(round(athlete.max_moment, Config.ROUNDING)),
            "max_lateral_velocity": str(round(athlete.max_lateral_velocity, Config.ROUNDING)),
            "lift_rate": str(round(athlete.lift_rate, Config.ROUNDING)),
            "num_minutes": athlete.num_minutes
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
                    "name": athlete["name"],
                    "gender": str(athlete["gender"]),
                    "warehouse": athlete["warehouse"],
                    "shift": athlete["shift"],
                    "job_function": athlete["job_function"],
                    "scores": []
                }
            )
        )

    athletes = []
    for athlete_id, athlete in athletes_by_id.iteritems():
        athletes_by_id[athlete_id]["score"] = avg(athlete["scores"], 1)
        del athletes_by_id[athlete_id]["scores"]
        athletes.append(athletes_by_id[athlete_id])

    athletes.sort(key=lambda data: data["score"]["avg_safety_score"], reverse=True)
    return athletes

def high_risk_info(athletes, athletes_count):
    high_risk = 0
    medium_risk = 0
    low_risk = 0
    high_risk_athletes_data = []
    med_risk_athletes_data = []
    low_risk_athletes_data = []

    for athlete in athletes:
        avg_safety_score = athlete["score"]["avg_safety_score"]
        if 0 <= avg_safety_score <= 40:
            high_risk += 1
            high_risk_athletes_data.append(athlete)
        elif 41 <= avg_safety_score <= 70:
            medium_risk += 1
            med_risk_athletes_data.append(athlete)
        elif 71 <= avg_safety_score <= 100:
            low_risk += 1
            low_risk_athletes_data.append(athlete)

    total_risk = high_risk + medium_risk + low_risk
    total_risk = total_risk - athletes_count if total_risk > athletes_count else 0
    high_risk += total_risk

    return {
        "total_athletes": athletes_count,
        "high_risk_athletes_percent" : round((float(high_risk) / athletes_count) * 100, Config.ROUNDING),
        "medium_risk_athletes_percent": round((float(medium_risk) / athletes_count) * 100, Config.ROUNDING),
        "low_risk_athletes_percent": round((float(low_risk) / athletes_count) * 100, Config.ROUNDING),
        "high_risk": high_risk_athletes_data,
        "medium_risk": med_risk_athletes_data,
        "low_risk": low_risk_athletes_data
    }


def campaign_all_data(client_id, warehouse_id, payload=None):
    if not client_id or not warehouse_id or not payload:
        return {
            "message": "please enter valid data"
        }

    start_date = None
    end_date = None
    campaign_id = int(payload["campaign_id"])

    if "start" in payload:
        try:
            start_date = int(payload["start"])
        except ValueError:
            start_date = datetime.datetime.strptime(payload["start"] , '%Y-%m-%d')

    if "end" in payload:
        try:
            end_date = int(payload["end"])
        except ValueError:
            end_date = datetime.datetime.strptime(payload["end"], '%Y-%m-%d')

    client_guid = db.db.session.query(db.Client.guid).filter(db.Client.id == client_id).scalar()
    campaign_details = {}

    campaign_query = db.db.session.query(db.Campaign).filter(
        db.Campaign.warehouse_id == warehouse_id,
        db.Campaign.id == campaign_id
    ).first()

    # overview of campaign
    if campaign_query:
        _start_date = None
        _end_date = None
        schema = CampaignSchema()
        campaign_details["overview"], _ = schema.dump(campaign_query)

        if start_date is None or not isinstance(start_date, datetime.date):
            _start_date = campaign_query.start_date
        else:
            _start_date = start_date.date()

        if end_date is None or not isinstance(end_date, datetime.date):
            _end_date = campaign_query.end_date
        else:
            _end_date = end_date.date()

        today = datetime.datetime.utcnow().date()
        # athletes_count = len(campaign_query.athletes) or 1

        if _end_date > today:
            _end_date = today - datetime.timedelta(days=1)

        kwargs = {
            "start_date": _start_date,
            "end_date": _end_date,
            "start_day": start_date,
            "end_day": end_date,
            "athletes": campaign_query.athletes,
            "client_guid": client_guid,
            "warehouse_id": warehouse_id,
            "campaign_id": campaign_id
        }

        campaign_details.update(get_athlete_score_per_day(**kwargs))
        campaign_details["athletes_per_group"] = get_athlete_score_per_group(**kwargs)

    return campaign_details

def get_athlete_score_per_day(**kwargs):
    from pipeline.db.questions.external_dashboard_queries.athletes import athletes
    athlete_ids = [athlete.id for athlete in kwargs.get('athletes', [])]

    return athletes(
        kwargs.get('client_guid'),
        range_start=kwargs.get('start_date'),
        range_end=kwargs.get('end_date'),
        warehouse_id=kwargs.get('warehouse_id'),
        athlete_ids=athlete_ids
    )


def get_athlete_score_per_group(**kwargs):
    athlete_ids = [athlete.id for athlete in kwargs.get('athletes', [])]
    groups = db.db.session.query(db.groups).filter(
        db.groups.c.industrial_athlete_id.in_(athlete_ids)
    )
    group_athlete_dict = {}
    for group in groups:
        if group.group_id not in group_athlete_dict:
            group_athlete_dict[group.group_id] = []

        group_athlete_dict[group.group_id].append(group.industrial_athlete_id)

    group_ids = group_athlete_dict.keys() or []
    groups = db.db.session.query(db.Group).filter(
        db.Group.id.in_(set(group_ids))
    )

    results = []

    for group in groups:
        athlete_ids = group_athlete_dict[group.id]
        if athlete_ids:
            query = get_athlete_query(
                athlete_ids=athlete_ids,
                range_start=kwargs.get('start_date'),
                range_end=kwargs.get('end_date'),
            )
            query = query.filter(
                db.Client.guid == kwargs.get('client_guid'),
                db.Warehouse.id == kwargs.get('warehouse_id')
            )
            query = query.group_by(
                db.IndustrialAthlete.id,
                db.ProcessedFile.id,
                db.Fuse.has_flx
            ).order_by('name', 'day')
            data = [row for row in query]

            all_athletes = get_all_athletes_scores(
                data, kwargs.get('start_date'), kwargs.get('end_date')
            )
            sort_by_date_for_all(all_athletes)
            results.append({
                "athlete_count": len(athlete_ids),
                "group_id": group.id,
                "group_name": group.name,
                "score": all_athletes
            })

    for index, group in enumerate(results):
        if group["score"] and len(group["score"]) > 0:
            count = len(group["score"])
            avg_twist_velocity = 0
            lift_rate = 0
            max_flexion = 0
            max_lateral_velocity = 0
            max_moment = 0
            safety_score = 0

            for score in group["score"]:
                avg_twist_velocity += float(score["avg_twist_velocity"])
                lift_rate += float(score["lift_rate"])
                max_flexion += float(score["max_flexion"])
                max_lateral_velocity += float(score["max_lateral_velocity"])
                max_moment += float(score["max_moment"])
                safety_score += float(score["safety_score"])

            score = {
                "avg_twist_velocity": round(float(avg_twist_velocity) / count, Config.ROUNDING),
                "avg_lift_rate": round(float(lift_rate) / count, Config.ROUNDING),
                "avg_max_flexion": round(float(max_flexion) / count, Config.ROUNDING),
                "avg_max_lateral_velocity": round(float(max_lateral_velocity) / count, Config.ROUNDING),
                "avg_max_moment": round(float(max_moment) / count, Config.ROUNDING),
                "avg_safety_score": round(float(safety_score) / count, Config.ROUNDING)
            }

            del results[index]["score"]
            results[index]["score"] = score

    return results
