from sat_orm.pipeline_orm.utilities import utils


def get_client_by_id(connection, client_id):
    """
    Get the Client via ID
    """
    db = utils.get_database_names()["pipeline"]
    client = connection.execute(
        "SELECT * FROM {}.client WHERE id={}".format(db, client_id)
    ).fetchone()
    return client


def get_client_by_name(connection, name):
    """
    Get the Client via Name
    """
    client = connection.execute(
        "SELECT * FROM client WHERE name='{}'".format(name)
    ).fetchone()
    return client