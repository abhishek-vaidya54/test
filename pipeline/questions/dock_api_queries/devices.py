from pipeline import db

def list_free_devices(warehouse_id):
    if not warehouse_id:
        return []

    fuse_query = db.db.session.query(db.Fuse.device_id)
    query = db.db.session.query(
        db.Device.id,
        db.Device.edison_id,
        db.Device.device_label,
        db.Device.hotspot_template,
        db.Device.hotspot,
        db.Device.start,
        db.Device.end
    ).filter(
        ~db.Device.id.in_(fuse_query)
    ).filter(
        db.Device.warehouse_id == warehouse_id
    )

    return [
        {
            'id': device.id,
            'edison_id': device.edison_id,
            'device_label': device.device_label,
            'hotspot_template': device.hotspot_template,
            'hotspot': device.hotspot,
            'start': device.start,
            'end': device.end,
        } for device in query
    ]


