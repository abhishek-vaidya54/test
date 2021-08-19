def get_shift(connection, shift_id, warehouse_id):
    """
    Helper method to retrieve the Shift object from the database
    Input:
        shift_id: Id of the shift
        warehouse_id: Id of the warehouse
    Output:
        shift: The Shift object retrieved from the database
    """
    shift = connection.execute(
        "SELECT * FROM shifts WHERE id={} AND warehouse_id={}".format(
            shift_id, warehouse_id
        )
    ).fetchone()

    return shift


def get_shift_by_name(connection, name):
    """
    Get the Shift via name
    """
    shift = connection.execute(f'SELECT * FROM shifts WHERE name="{name}"').fetchone()

    return shift