
from dataclasses import dataclass


@dataclass
class DbUrl:
    """The Data object for database connection.

    Args:
        driver: The name of the driver. At the moment `psycopg2` support only.
        host: The host of the database. For example `localhost`.
        port: The port of the database. For example `5432`.
        database: The database name. For example `test`.
        user: The user name of database. For example `root`.
        password: The pasword to database. For example `1234`.
    """
    driver: str
    host: str
    port: str
    database: str
    user: str
    password: str
