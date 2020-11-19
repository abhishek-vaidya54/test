def get_client_by_id(connection, client_id):
    """
    Get the Client via ID
    """
    client = connection.execute(
        "SELECT * FROM pipeline.client WHERE id={}".format(client_id)
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