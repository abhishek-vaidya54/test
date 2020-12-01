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