from pipeline import db
import sqlalchemy as sa

from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound
from pipeline.db.questions.external_dashboard_queries.utils import apply_warehouse_filter_athletes, apply_warehouses_filter

def _get_athletes_query(dock_user=None, athlete_id=None):
    query = db.db.session.query(
        db.IndustrialAthlete.id.label('id'),
        db.IndustrialAthlete.name.label('name'),
        db.IndustrialAthlete.first_name.label('first_name'),
        db.IndustrialAthlete.last_name.label('last_name'),
        db.IndustrialAthlete.external_id.label('external_id'),
        db.IndustrialAthlete.available.label('available'),
        db.IndustrialAthlete.has_haptic.label('has_haptic')
    ).order_by('name asc')

    if dock_user:
        query = apply_warehouses_filter(query, dock_user.warehouses)

    if athlete_id:
        query = query.filter(db.IndustrialAthlete.id == athlete_id)

    return query


# returns a boolean, 'True' means use first_name+last_name for name field, 'False' means use external_id
def get_display_name_property(warehouse_id):
    query = db.db.session.query(
                    db.Warehouse.display_names.label('display_names'),
                ).filter(
                    db.Warehouse.id == warehouse_id
                ).one_or_none()

    if not query:
        return None

    return query.display_names

# returns a list of athletes and their availability/haptic status
def list_athletes(dock_user):
    query = _get_athletes_query(dock_user=dock_user)

    if not query:
        return []

    return get_athletes_payload(query, dock_user)



def get_athlete(athlete_id):
    if athlete_id:
        query = _get_athletes_query(athlete_id=athlete_id)
        return get_athletes_payload(query)

    return []


# returns the response payload sent to the dock
def get_athletes_payload(query, dock_user = None):

    if not query:
        return []

    if dock_user:
        warehouses = dock_user.warehouses
        if len(warehouses) > 0:
            warehouse_ids = map(lambda x: x.id, warehouses)
            warehouse_id = warehouse_ids[0]

    # if there is no dock user, use the first athletes warehouse_id
    else:
        warehouse_id = query[0].warehouse_id


    # check if this warehouse allows full athlete names to be displayed
    should_display_names = get_display_name_property(warehouse_id)

    if should_display_names:
        return [{
            'id': athlete.id,
            'name': (athlete.first_name + ' ' + athlete.last_name).rstrip(),
            'available': athlete.available,
            'has_haptic': athlete.has_haptic
        } for athlete in query]

    # if a warehouse doesn't allow full athlete names to be displayed, use external id field
    else:
        return [{
            'id': athlete.id,
            'name': athlete.external_id,
            'available': athlete.available,
            'has_haptic': athlete.has_haptic
        } for athlete in query]




def get_count_athletes(dock_user):
    query = db.db.session.query(sa.func.count(db.IndustrialAthlete.id))
    query = apply_warehouses_filter(query, dock_user.warehouses)

    return {
        "athlete_count": query.scalar()
    }


def update_athlete(athlete_id, is_available):
    available = True if is_available and is_available == 1 else False
    print "is_available", is_available
    if athlete_id:
        try:
            query = db.db.session.query(
                db.IndustrialAthlete.id.label('id'),
                db.IndustrialAthlete.name.label('name'),
                db.IndustrialAthlete.available.label('available')
            ).filter(
                db.IndustrialAthlete.id == athlete_id
            ).order_by('name asc').one()

            db.db.session.query(db.IndustrialAthlete).filter(
                db.IndustrialAthlete.id == query[0]
            ).update({"available": available})
            db.db.session.commit()
            db.db.session.flush()

            return {
                'id': query[0],
                'name': query[1],
                'available': available
            }
        except NoResultFound:
            return {
                'message': "No athlete found"
            }

    return {
        'message': "Please add correct information"
    }
