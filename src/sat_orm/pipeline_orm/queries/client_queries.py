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
    client = connection.execute(f'SELECT * FROM client WHERE name=\"{name}\"').fetchone()
    return client


def get_client_exists(connection, client_id):
    """
    Helper method to retrieve the Client object from the database
    Input:
        client_id: Id of a client
    Output:
        client: The client object retrieved from the database
    """
    client = connection.execute(
        "SELECT * FROM client WHERE id='{}'".format(client_id)
    ).scalar()
    return client