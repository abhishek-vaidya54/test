from sat_orm.pipeline_orm.utilities import utils


def get_dock_exists(session, dock_id):
    """
    Helper method to retrieve the DockPhase object from the database
    Input:
        dock: Id of a dock
    Output:
        dock: The dock object retrieved from the database
    """

    db_names = utils.get_database_names()
    query = "SELECT * FROM {}.config WHERE {}.config.dock_id='{}'".format(
        db_names["dockv5"], db_names["dockv5"], dock_id
    )
    dock = session.execute(query).fetchone()
    return dock
