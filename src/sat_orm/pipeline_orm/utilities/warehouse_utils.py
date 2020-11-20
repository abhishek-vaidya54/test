
def is_valid_lat_long(key, value):
    """
    Helper method that checks if input is valid latitude or longitude
    """
    try:
        parsed = float(value)
        if key == "latitude":
            return parsed >= -90 and parsed <= 90
        else:
            return parsed >= -180 and parsed <= 180
    except:
        return False

def is_valid_lat_long_direction(value):
    return value in ("N", "S", "E", "W")