import sqlite3

from typing import Any
from ...connection import Connectin
from ...db_url import DbUrl


class SQLite3Connection(Connectin):
    """sqlite3 Connection implementation."""

    def connect(self, url: DbUrl) -> Any:
        self.connection = sqlite3.connect(url.database, detect_types=sqlite3.PARSE_DECLTYPES |
                                          sqlite3.PARSE_COLNAMES)
        return self.connection

    def close(self):
        self.connection.close()
