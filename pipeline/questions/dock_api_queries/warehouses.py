from pipeline import db


def warehouses(client_guid):
    """Give all warehouses of a given client."""

    query = (
        db.db.session.query(
            db.Warehouse.id.label("id"),
            db.Warehouse.name.label("name"),
            db.Warehouse.location.label("location"),
        )
        .join(db.Client)
        .filter(db.Client.guid == client_guid)
    )

    warehouse_info = []
    for warehouse in query:
        warehouse_info.append(
            {"id": warehouse.id, "name": warehouse.name, "location": warehouse.location}
        )

    return warehouse_info
