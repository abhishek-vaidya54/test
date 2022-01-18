from pipeline import db
from pipeline.server.schemas import GroupSchema

from pipeline.db.questions.external_dashboard_queries.utils import (
    apply_warehouse_filter,
)


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


def warehouse_groups(warehouse_id):
    query = db.db.session.query(db.Group)
    query = apply_warehouse_filter(query, warehouse_id, column=db.Group.warehouse_id)

    groups, _ = GroupSchema().dump(query, many=True)
    return groups
