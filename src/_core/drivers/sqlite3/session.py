from typing import Any, List, Tuple

from ...session import Session


class SQLite3Sesion(Session):
    """Psycopg2 Session implementation."""

    def connect(self):
        super().connect()
        self._cursor = self._connection.cursor()

    def __iter__(self):
        self.connect()
        return self

    def __next__(self):
        self.disconnect()
        return self

    def disconnect(self):
        super().disconnect()
        self._cursor.close()

    def execute(self, sql: str):
        self._cursor.execute(sql)

    def commit(self):
        self._connection.commit()

    def fetch_one(self, sql: str) -> Tuple[Any] | None:
        self._cursor.execute(sql)
        result = self._cursor.fetchone()
        return result

    def fetch_all(self, sql: str) -> List[Tuple[str, Any]]:
        self._cursor.execute(sql)
        result = self._cursor.fetchall()
        return result
