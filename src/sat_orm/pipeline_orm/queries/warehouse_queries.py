def get_warehouse(connection, warehouse_id):
    """
    Helper method to retrieve the Warehouse object from the database
    Input:
        warehouse_id: Id of the warehouse
    Output:
        warehouse: The Warehouse object retrieved from the database
    """
    warehouse = connection.execute(
        "SELECT * FROM pipeline.warehouse WHERE id={}".format(warehouse_id)
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