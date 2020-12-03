from sat_orm.pipeline_orm.utilities import utils


def get_warehouse(connection, warehouse_id, client_id=None):
    """
    Helper method to retrieve the Warehouse object from the database
    Input:
        warehouse_id: Id of the warehouse
        client_id: Id of the client
    Output:
        warehouse: The Warehouse object retrieved from the database
    """
    db = utils.get_database_names()["pipeline"]
    warehouse = {}
    if client_id is None:
        warehouse = connection.execute(
            "SELECT * FROM {}.warehouse WHERE id={}".format(db, warehouse_id)
        ).fetchone()
    else:
        warehouse = connection.execute(
            "SELECT * FROM {}.warehouse WHERE id={} AND client_id={}".format(
                db, warehouse_id, client_id
            )
        ).fetchone()
        print("Wa1 ", warehouse)

    return warehouse


def get_warehouse_exists(connection, warehouse_id):
    """
    Helper method to retrieve the warehouse object from the database
    Input:
        warehouse_id: Id of a warehouse
    Output:
        warehouse: The warehouse object retrieved from the database
    """
    db = utils.get_database_names()["pipeline"]
    warehouse = connection.execute(
        "SELECT * FROM {}.warehouse WHERE id={}".format(db, warehouse_id)
    ).fetchone()

    return warehouse
