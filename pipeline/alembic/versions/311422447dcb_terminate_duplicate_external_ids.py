"""terminate duplicate external ids

Revision ID: 311422447dcb
Revises: 75c576d02328
Create Date: 2020-10-22 13:55:52.945949

"""
from alembic import op
from datetime import datetime, time, timedelta
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

    midnight_epoch = datetime.combine(datetime.today(), time.min).timestamp()
    for index, record in list(enumerate(result)):
        if index + 1 == len(result):
            break
        if (
            record["external_id"] == result[index + 1]["external_id"]
            and record["warehouse_id"] == result[index + 1]["warehouse_id"]
        ):
            current_id = record["id"]
            new_timestamp = midnight_epoch + index

            sql = f"""
                    UPDATE industrial_athlete
                    SET termination_date = FROM_UNIXTIME({new_timestamp})
                    WHERE id={current_id}
                """
            op.execute(sql)

    query = """
                SELECT t1.id, t1.client_id, t1.warehouse_id, t1.external_id, t1.termination_date
                FROM pipeline.industrial_athlete t1
                JOIN (
                    SELECT external_id, warehouse_id
                    FROM pipeline.industrial_athlete
                    WHERE termination_date is not null
                    GROUP BY external_id, warehouse_id, termination_date
                    HAVING COUNT(*) > 1
                ) t2 ON t1.external_id = t2.external_id AND t1.warehouse_id = t2.warehouse_id AND termination_date is not null
                ORDER BY t1.external_id, t1.id asc
            """
    result = connection.execute(query).fetchall()

    for index, record in list(enumerate(result)):
        current_id = record["id"]
        new_timestamp = (
            datetime.combine(record["termination_date"], time.min)
            + timedelta(seconds=index + 1)
        ).timestamp()

        sql = f"""
                UPDATE industrial_athlete 
                SET termination_date = FROM_UNIXTIME({new_timestamp})
                WHERE id={current_id}
            """

        op.execute(sql)

    # 10659,10710,10711,10712,9906,9908,9809,10728,9884,10693,9901,10809,10680,10802,10683,10800,10682,10799,9880,9882,10726,10795,10679,10798,10672,10803,10697,10788,22889,22948,10685,10780,22884,22949,10684,10785,21951,22063,21950,22068,22839,22843,9890,9892,9876,10812,10694,10810,9985,10673,9824,10687,10832,10856,23056,23062,10731,10772,22395,22493,22396,22494,9813,10807,10730,10773,30828,30833,9729,10648,9747,10138,10675,10814,10894,21948,10033,21859,10681,10801,9919,10208,10047,10792,21945,21947,9844,22865
    query = """
                SELECT t1.id, t1.hire_date, t1.external_id, t1.warehouse_id, t1.termination_date
                FROM pipeline.industrial_athlete t1
                JOIN (
                    SELECT external_id, warehouse_id
                    FROM pipeline.industrial_athlete
                    WHERE warehouse_id IN (43, 44, 68, 69)
                    AND termination_date is null
                    GROUP BY external_id, warehouse_id
                    HAVING COUNT(*) > 1
                ) t2 ON t1.external_id = t2.external_id AND t1.warehouse_id = t2.warehouse_id
                ORDER BY t1.external_id, t1.id asc
            """
    result = connection.execute(query).fetchall()

    midnight_epoch = datetime.combine(datetime.today(), time.min).timestamp()
    for index, record in list(enumerate(result)):
        if index + 1 == len(result):
            break
        if (
            record["external_id"] == result[index + 1]["external_id"]
            and record["warehouse_id"] == result[index + 1]["warehouse_id"]
        ):
            current_id = record["id"]
            new_timestamp = midnight_epoch + index

            sql = f"""
                    UPDATE industrial_athlete
                    SET termination_date = FROM_UNIXTIME({new_timestamp})
                    WHERE id={current_id}
                """
            op.execute(sql)

    # raise "Test"


def downgrade():
    pass
