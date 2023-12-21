from abc import ABC
from ..errors import UnknownDriverError

from .sql_adapter import SqlAdapter

from .psycopg2.sql_adapter import Psycopg2SqlAdapter
from .psycopg2.constants import DRIVER_NAME as PSYCOPG2_DRIVER_NAME

from .sqlite3.sql_adapter import SqLite3SqlAdapter
from .sqlite3.constants import DRIVER_NAME as SQLITE3_DRIVER_NAME


class SqlAdapterFactory(ABC):
    """The SQL adapter factory."""

    def create(driver: str) -> SqlAdapter:
        """Create `SqlAdapter` by driver name.

        Args:
            driver: The name of the driver.

        Raises:
            UnknownDriverError: If the driver is unknown.
        """
        if driver == PSYCOPG2_DRIVER_NAME:
            return Psycopg2SqlAdapter()
        elif driver == SQLITE3_DRIVER_NAME:
            return SqLite3SqlAdapter()

        raise UnknownDriverError(f'unkknown driver {driver}')
