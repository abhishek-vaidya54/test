def get_client_by_id(connection, client_id):
    """
    Get the Client via ID
    """
    client = connection.execute(
        "SELECT * FROM client WHERE id={}".format(client_id)
    ).fetchone()
    return client