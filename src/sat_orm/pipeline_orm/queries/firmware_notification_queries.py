from sat_orm.pipeline_orm.utilities import utils


def get_firmware_notification_exists(connection, notification_id):
    """
    Helper method to retrieve the Notification object from the database
    Input:
        notification_id: Id of a firmware notification
    Output:
        notification: The notification object retrieved from the database
    """
    notification = connection.execute(
        "select * from Notification where id={}".format(notification_id)
    ).fetchone()
    return notification
