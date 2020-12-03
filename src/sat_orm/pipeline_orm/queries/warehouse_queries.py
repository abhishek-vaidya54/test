from sat_orm.pipeline_orm.utilities import utils


def get_warehouse(connection, warehouse_id):
    """
    Helper method to retrieve the Warehouse object from the database
    Input:
        warehouse_id: Id of the warehouse
        client_id: Id of the client
    Output:
        warehouse: The Warehouse object retrieved from the database
    """
    db = utils.get_database_names()["pipeline"]
    warehouse = connection.execute(
        "SELECT * FROM {}.warehouse WHERE id={}".format(db, warehouse_id)
    ).fetchone()

    return warehouse
