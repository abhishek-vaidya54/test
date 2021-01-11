def get_user_by_id(connection, user_id):
    """
    Helper method to retrieve the user object from the database
    Input:
        user_id: Id of a user
    Output:
        user: The user object retrieved from the database
    """
    user = connection.execute(
        "SELECT * FROM external_admin_user WHERE id='{}'".format(user_id)
    ).fetchone()
    return user