import datetime

from pipeline.config import Config
from webargs import missing
from pipeline import db
from sqlalchemy.sql.expression import desc, asc
import operator

YEAR = 365

def generate_scores(query, sorting_order):
    data = _generate_data(query)

    result = {}
    for k, v in data.items():
        if not result:
            result = v
        elif result['safety_score']:
            v_safety_score = v['safety_score']/v['total_rows']
            result_safety_score = result['safety_score']/result['total_rows']
            
            if sorting_order == "desc" and v_safety_score < result_safety_score:
                result = v
            elif sorting_order == "asc" and v_safety_score > result_safety_score:
                result = v

    athlete_count = len(result['athletes'])
    scores = {}
    scores["id"] = result['id']
    scores["name"] = result['name']
    scores["safety_score"] = str(round(result['safety_score'] / result['total_rows'], Config.ROUNDING))
    scores["avg_twist_velocity"] = str(round(result['avg_twist_velocity'] / result['total_rows'], Config.ROUNDING))
    scores["max_flexion"] = str(round(result['max_flexion'] / result['total_rows'], Config.ROUNDING))
    scores["max_moment"] = str(round(result['max_moment'] / result['total_rows'], Config.ROUNDING))
    scores["max_lateral_velocity"] = str(round(result['max_lateral_velocity'] / result['total_rows'], Config.ROUNDING))
    scores["lift_rate"] = str(round(result['lift_rate'] / result['total_rows'], Config.ROUNDING))
    scores["total_athletes"] = str(athlete_count)

    return scores


def generate_daily_scores(query):
    scores = {}
    for row in query:
        if row.id not in scores:
            scores[row.id] = {
                    "id": row.id,
                    "name": row.name,
                    "scores": []
                    }

    data = {}

    for row in query:
        if row.day not in data:
            data[row.day] = generate_single_row(row)
        else:
            if row.id not in data[row.day]:
                data[row.day].update(generate_single_row(row))
            else:
                data[row.day][row.id]['id'] = row.id
                data[row.day][row.id]['total_rows'] += 1
                data[row.day][row.id]['total_athletes'].add(row.aid)
                data[row.day][row.id]['safety_score'] += row.safety_score
                data[row.day][row.id]['max_flexion'] += row.max_flexion
                data[row.day][row.id]['avg_twist_velocity'] += row.avg_twist_velocity
                data[row.day][row.id]['max_moment'] += row.max_moment
                data[row.day][row.id]['max_lateral_velocity'] += row.max_lateral_velocity
                data[row.day][row.id]['lift_rate'] += row.lift_rate
                data[row.day][row.id]['day'] = str(row.day)
                data[row.day][row.id]['athlete_name'] = str(row.athlete_name)
                data[row.day][row.id]['athlete_id'] = row.aid
                data[row.day][row.id]['athlete_hire_date'] = str(row.athlete_hire_date)

    for _, d in data.items():
        for _, v in d.items():
            if v['id'] in scores:
                scores[v['id']]['scores'].append({
                    'total_athletes': len(v['total_athletes']),
                    'safety_score': str(round(v['safety_score'] / v['total_rows'], Config.ROUNDING)),
                    'max_flexion': str(round(v['max_flexion'] / v['total_rows'], Config.ROUNDING)),
                    'avg_twist_velocity': str(round(v['avg_twist_velocity'] / v['total_rows'], Config.ROUNDING)),
                    'max_moment': str(round(v['max_moment'] / v['total_rows'], Config.ROUNDING)),
                    'max_lateral_velocity': str(round(v['max_lateral_velocity'] / v['total_rows'], Config.ROUNDING)),
                    'lift_rate': str(round(v['lift_rate'] / v['total_rows'], Config.ROUNDING)),
                    'day': str(v['day']),
                    'athlete_id': v['athlete_id'],
                    'athlete_name': v['athlete_name'],
                    'athlete_hire_date': v['athlete_hire_date'],
                })

    for id in scores:
        scores[id]['scores'].sort(key=operator.itemgetter('day'))

    return scores


def generate_single_row(row):
    return {
        row.id: {
            'id': row.id,
            'total_rows': 1,
            'total_athletes': _set_athletes_count(row.aid),
            'safety_score': row.safety_score,
            'max_flexion': row.max_flexion,
            'avg_twist_velocity': row.avg_twist_velocity,
            'max_moment': row.max_moment,
            'max_lateral_velocity': row.max_lateral_velocity,
            'lift_rate': row.lift_rate,
            'day': str(row.day),
            'athlete_id': row.aid,
            'athlete_name': row.athlete_name,
            'athlete_hire_date': str(row.athlete_hire_date),
        }
    }


def _generate_data(query):
    data = {}
    for row in query:
        if row.id not in data:
            data[row.id] = {
                'id': row.id,
                'name': row.name,
                'athletes': _set_athletes_count(row.aid),
                'total_rows': 1,
                'safety_score': row.safety_score,
                'max_flexion': row.max_flexion,
                'avg_twist_velocity': row.avg_twist_velocity,
                'max_moment': row.max_moment,
                'max_lateral_velocity': row.max_lateral_velocity,
                'lift_rate': row.lift_rate
            }
        else:
            data[row.id]['id'] = row.id
            data[row.id]['name'] = row.name
            data[row.id]['athletes'].add(row.aid)
            data[row.id]['total_rows'] += 1
            data[row.id]['safety_score'] += row.safety_score
            data[row.id]['max_flexion'] += row.max_flexion
            data[row.id]['avg_twist_velocity'] += row.avg_twist_velocity
            data[row.id]['max_moment'] += row.max_moment
            data[row.id]['max_lateral_velocity'] += row.max_lateral_velocity
            data[row.id]['lift_rate'] += row.lift_rate

    return data


def get_latest_risk_query(client_id=None):
    query = db.db.session.query(db.Risk.start_time).join(
        db.ProcessedFile,
        db.Fuse,
        db.IndustrialAthlete,
        db.Warehouse,
        db.Client,
    ).filter(
        db.ProcessedFile.version == Config.ALGO_VERSION,
        db.Client.id == client_id
    ).order_by(desc(db.Risk.start_time)).limit(1)

    return query
    

def get_date_range(client_id, range_start, range_end, range_days=YEAR):
    if range_start is missing and range_end is missing:
        risk = get_latest_risk_query(client_id=client_id).first()
        if risk is None:
            range_end = datetime.datetime.now()
            range_start = range_end - datetime.timedelta(days = range_days)
            return range_start, range_end
        date = risk.start_time.date()

        range_start = date - datetime.timedelta(days = range_days)
        
        range_end = risk.start_time.date()
    return range_start, range_end

def apply_warehouse_filter(query, warehouse_id, column=db.IndustrialAthlete.warehouse_id):
    if warehouse_id:
        query = query.filter(column == warehouse_id)
    return query

def apply_warehouse_filter_athletes(query, warehouse_id):
    return apply_warehouse_filter(query, warehouse_id)

def apply_warehouses_filter(query, warehouses):
    if len(warehouses) > 0:
        warehouse_ids = map(lambda x: x.id, warehouses)
        query = query.filter(db.IndustrialAthlete.warehouse_id.in_(warehouse_ids))
    return query

def _set_athletes_count(aid):
    athletes = set()
    athletes.add(aid)
    return athletes

