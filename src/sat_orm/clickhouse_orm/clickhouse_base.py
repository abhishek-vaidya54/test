import os
from contextlib import contextmanager
import logging

from clickhouse_driver import Client


logging.basicConfig()
LOGGER = logging.getLogger()


@contextmanager
def get_client():
    clickhouse_url = os.environ.get("CLICKHOUSE_URL", None)
    clickhouse_password = os.environ.get("CLICKHOUSE_PASSWORD", None)

    if clickhouse_url is None or clickhouse_password is None:
        raise Exception("DB env variables cannot be None.")

    client = Client(
        clickhouse_url,
        user="admin",
        password=clickhouse_password,
        port=9440,
        secure="y",
        verify=False,
    )

    try:
        yield client
    except Exception as exception:
        print("exception: ", exception)
        LOGGER.exception(exception)

        raise exception  # If exception isn't raised again, response is 200
    finally:
        client.disconnect()
