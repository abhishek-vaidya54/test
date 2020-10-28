def get_warehouse(connection, warehouse_id, client_id):
    """
    Helper method to retrieve the Warehouse object from the database
    Input:
        client_id: Id of the client
        warehouse_id: Id of the warehouse
    Output:
        warehouse: The Warehouse object retrieved from the database
    """
    if client_id is None:
        warehouse = connection.execute(
            "SELECT * FROM warehouse WHERE id='{}'".format(warehouse_id)
        ).fetchone()
    else:
        warehouse = connection.execute(
            "SELECT * FROM warehouse WHERE id={} and client_id={}".format(
                warehouse_id, client_id
            )
        ).fetchone()
    return warehouse