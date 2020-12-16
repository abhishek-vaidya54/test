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


def get_target_by_id(connection, target_type, target_id):
    """
    Helper method to retrieve the target object from the database
    Input:
        target_id: Id of the target
        target_type: Can be 'group', 'warehouse', 'industrial_athlete'
    Output:
        target: The target object retrieved from the database
    """
    target = connection.execute(
        "SELECT * FROM pipeline.{} WHERE id={}".format(
            target_type if target_type != "group" else "groups", target_id
        )
    ).fetchone()

    return target