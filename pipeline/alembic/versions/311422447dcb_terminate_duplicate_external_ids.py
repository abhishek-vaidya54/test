"""terminate duplicate external ids

Revision ID: 311422447dcb
Revises: 75c576d02328
Create Date: 2020-10-22 13:55:52.945949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "311422447dcb"
down_revision = "7a120d5585f5"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()

    query = """
                SELECT t1.id, t1.hire_date, t1.external_id, t1.warehouse_id, t1.termination_date
                FROM pipeline.industrial_athlete t1
                JOIN (
                    SELECT external_id, warehouse_id
                    FROM pipeline.industrial_athlete
                    WHERE client_id IN (41, 44, 47, 50, 52, 62, 90, 91, 93, 94, 98, 99, 100, 109, 110, 115, 119, 120, 121)
                    AND termination_date is null
                    GROUP BY external_id, warehouse_id
                    HAVING COUNT(*) > 1
                ) t2 ON t1.external_id = t2.external_id AND t1.warehouse_id = t2.warehouse_id
                ORDER BY t1.external_id, t1.id asc
            """
    result = connection.execute(query).fetchall()

    ids_to_update = []
    for index, record in list(enumerate(result)):
        if index + 1 == len(result):
            break
        if (
            record["external_id"] == result[index + 1]["external_id"]
            and record["warehouse_id"] == result[index + 1]["warehouse_id"]
        ):
            ids_to_update.append(record["id"])

    op.execute(
        """
            UPDATE industrial_athlete 
            SET termination_date = FROM_UNIXTIME(UNIX_TIMESTAMP() - id)
            WHERE id IN {}
        """.format(
            tuple(ids_to_update)
        )
    )


def downgrade():
    pass
