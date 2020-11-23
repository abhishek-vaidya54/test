def get_warehouse(connection, warehouse_id, client_id=None):
    """
    Helper method to retrieve the Warehouse object from the database
    Input:
        warehouse_id: Id of the warehouse
        client_id: Id of the client
    Output:
        warehouse: The Warehouse object retrieved from the database
    """
    warehouse = {}
    if client_id is None:
        warehouse = connection.execute(
            "SELECT * FROM pipeline.warehouse WHERE id={}".format(warehouse_id)
        ).fetchone()
    else:
        warehouse = connection.execute(
            "SELECT * FROM pipeline.warehouse WHERE id={} AND client_id={}".format(warehouse_id, client_id)
        ).fetchone()

    return warehouse

def get_warehouse_exists(connection, warehouse_id):
    """
    Helper method to retrieve the warehouse object from the database
    Input:
        warehouse_id: Id of a warehouse
    Output:
        warehouse: The warehouse object retrieved from the database
    """
    warehouse = connection.execute(
        "SELECT * FROM pipeline.warehouse WHERE id={}".format(warehouse_id)
    ).scalar()
    return warehouse