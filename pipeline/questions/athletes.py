import sqlalchemy as sa

from pipeline.config import Config
from pipeline import db
from pipeline.db.processed_file import COMPLETE


def get_athlete_query(client_guid):
    query = (
        db.db.session.query(
            sa.func.count(sa.func.distinct(sa.func.DATE(db.Risk.start_time))).label(
                "days_of_data"
            ),
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
        .filter(
            db.ProcessedFile.version == Config.ALGO_VERSION,
            db.ProcessedFile.status == COMPLETE,
        )
        .filter(db.Client.guid == client_guid)
        .group_by(db.IndustrialAthlete.id, db.IndustrialAthlete.name, db.Fuse.has_flx)
        .order_by(db.IndustrialAthlete.name, db.Fuse.has_flx)
    )

    return query


def athletes(client_guid):

    query = get_athlete_query(client_guid)

    db_athletes_by_id = {
        ia.id: ia
        for ia in db.db.session()
        .query(db.IndustrialAthlete)
        .join(db.Client)
        .filter(db.Client.guid == client_guid)
    }
    athletes_by_id = {}
    for athlete_data in query:
        has_flx = bool(athlete_data.has_flx)
        db_athlete = db_athletes_by_id[athlete_data.id]
        athlete = athletes_by_id.setdefault(
            athlete_data.id,
            {
                "id": athlete_data.id,
                "name": athlete_data.name,
                "tags": [tag.name for tag in db_athlete.tags],
                "flx_count": 0,
                "no_flx_count": 0,
            },
        )
        if has_flx:
            athlete["flx_count"] = athlete_data.days_of_data
        else:
            athlete["no_flx_count"] = athlete_data.days_of_data

    return athletes_by_id.values()
