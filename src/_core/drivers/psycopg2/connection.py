import psycopg2

from typing import Any
from ...connection import Connectin
from ...db_url import DbUrl


class Psycopg2Connection(Connectin):
    """Psycopg2 Connection implementation."""

    def connect(self, url: DbUrl) -> Any:
        self.connection = psycopg2.connect(
            f"dbname='{url.database}' host='{url.host}' port='{url.port}' user='{url.user}' password='{url.password}'")
        return self.connection

    def close(self):
        self.connection.close()
