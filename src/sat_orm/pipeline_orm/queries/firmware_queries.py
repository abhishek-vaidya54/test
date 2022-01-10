def get_device_type_by_id(connection, device_type_id):
    """
    Helper method to retrieve the user object from the database
    Input:
        device_type_id: Id of a device_type
    Output:
        device_type: The device_type object retrieved from the database
    """
    device_type = connection.execute(
        "SELECT * FROM device_type WHERE id='{}'".format(device_type_id)
    ).fetchone()
    return device_type


def get_hardware_by_id(connection, hardware_id):
    """
    Helper method to retrieve the user object from the database
    Input:
        hardware_id: Id of a hardware
    Output:
        hardware: The hardware object retrieved from the database
    """
    hardware = connection.execute(
        "SELECT * FROM hardware WHERE id='{}'".format(hardware_id)
    ).fetchone()
    return hardware


def get_firmware_exists(connection, firmware_id):
    """
    Helper method to retrieve the Notification object from the database
    Input:
        firmware_id: Id of a firmware
    Output:
        firmware: The firmware object retrieved from the database
    """
    firmware = connection.execute(
        "select * from firmware where id={}".format(firmware_id)
    ).fetchone()
    return firmware
