from abc import ABC
from typing import Any

from ..session import Session
from ..errors import UnknownDriverError
from .sql_adapter import SqlAdapter

from .psycopg2.constants import DRIVER_NAME as PSYCOPG2_DRIVER_NAME
from .psycopg2.session import Psycopg2Sesion


class SessionFactory(ABC):
    """The Session factory."""

    def create(driver: str, connection: Any, adapter: SqlAdapter) -> Session:
        """Create `Session` by driver name.

        Args:
            driver: The name of the driver.
            connection: The connection to database.
            adapter: The SQL adapter for creating queries.

        Raises:
            UnknownDriverError: If the driver is unknown.
        """
        if driver == PSYCOPG2_DRIVER_NAME:
            return Psycopg2Sesion(connection, adapter)

        raise UnknownDriverError(f'unkknown driver {driver}')
