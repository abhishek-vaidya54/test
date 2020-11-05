def get_setting(connection, settings_id):
    """
    Helper method to retrieve the Warehouse object from the database
    Input:
        client_id: Id of the client
        warehouse_id: Id of the warehouse
    Output:
        warehouse: The Warehouse object retrieved from the database
    """
    setting = connection.execute(
        "SELECT * FROM settings WHERE id={}".format(settings_id)
    ).fetchone()

    return setting