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