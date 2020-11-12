def get_ia_by_external_id(connection, external_id, warehouse_id):
    """
        Helper method to retrieve the IA object from the database
        Input:
            external_id: External Id of an industrial athlete
            warehouse_id: Id of the warehouse
    :
            user: The IA object retrieved from the database
    """
    ia = connection.execute(
        "SELECT * FROM industrial_athlete WHERE external_id='{}' AND warehouse_id={} AND termination_date IS NULL".format(
            external_id, warehouse_id
        )
    ).fetchone()
    return ia
