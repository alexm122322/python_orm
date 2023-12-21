from abc import ABC
from ..connection import Connectin
from ..errors import UnknownDriverError

from .psycopg2.connection import Psycopg2Connection
from .psycopg2.constants import DRIVER_NAME as PSYCOPG2_DRIVER_NAME

from .sqlite3.connection import SQLite3Connection
from .sqlite3.constants import DRIVER_NAME as SQLITE3_DRIVER_NAME


class ConnectionFactory(ABC):
    """The Connection factory."""
    def create(driver: str) -> Connectin:
        """Create `Connectin` by driver name.

        Args:
            driver: The name of the driver.

        Raises:
            UnknownDriverError: If the driver is unknown.
        """
        if driver == PSYCOPG2_DRIVER_NAME:
            return Psycopg2Connection()
        elif driver == SQLITE3_DRIVER_NAME:
            return SQLite3Connection()

        raise UnknownDriverError(f'unkknown driver {driver}')
