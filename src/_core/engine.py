from types import FunctionType, MethodType
from typing import List
from .drivers.sql_adapter_factory import SqlAdapterFactory
from .drivers.session_factory import SessionFactory
from .drivers.connection_factory import ConnectionFactory

from .db_url import DbUrl
from .session import Session
from .orm_db_version import OrmDBVersion
from .ddl.model import Model
from .ddl.migration import Migration


def _on_update(migration: Migration, old_version: int, current_version: int):
    """On Ugrade tamplate.

    Args:
        migration: The object with migration methods.
        old_version: The old version of database.
        current_version: The current version of database. 
    """
    pass

def _on_create(create_table: FunctionType| MethodType):
    """On Create temlate
    
    Args:
        create_table: Function for creating tables. 
    """
    pass


class Engine:
    """The Engine of python_orm package. 
    Engine connecting to the database and create `connection`. 
    Check out the `_connect_to_db` function.

    Args:
        url: The object of database url.
        version: The version of the database. For migration purposes.
         0 by default.
        on_create: Callback for tables creations. Check out the `_on_create` function.
        on_update: Callback for migration. Check out the `_on_update` function.
        connect: The object for connection.
        connection: The connection with the database.
        adapter: The SQL adapter. Contains methods and properties with SQL languages.
    """

    def __init__(self, url: DbUrl, version: int = 0, on_create: FunctionType = _on_create,
                 on_update: FunctionType = _on_update):
        self._url = url
        self.version = version
        self._on_update = on_update
        self._on_create = on_create
        self._connect_to_db()
        self.adapter = SqlAdapterFactory.create(self.driver)
        self._migrate()

    def drop_all_tables(self):
        """Drops all tables in the table."""
        seesion_obj = SessionFactory.create(
            self.driver, self.connection, self.adapter)
        with seesion_obj as session:
            session.execute(self.adapter.clear_database)
            session.commit()

    def create_tables(self, tables: List[Model]):
        """Creates all tables connected to the module."""
        seesion_obj = SessionFactory.create(
            self.driver, self.connection, self.adapter)
        with seesion_obj as session:
            for item in tables:
                session.create_table(item)

    def disconnect(self):
        """Disconnected from the database. Closes connection."""
        self.connect.close()

    def _connect_to_db(self):
        """Creates connection with the database."""
        self.connect = ConnectionFactory.create(self.driver)
        self.connection = self.connect.connect(self._url)

    def _migrate(self):
        """Migration flow."""
        seesion_obj = SessionFactory.create(
            self.driver, self.connection, self.adapter)
        with seesion_obj as session:
            self._init_version_table(session)
            self._run_migration(session)

    def _init_version_table(self, session: Session):
        """Initialization of the table version.

        Args:
            session: For executing SQL queries.
        """
        session.create_table(OrmDBVersion)
        value = session.query(OrmDBVersion).first()
        if value is None:
            self._on_create(self.create_tables)
            session.insert_item(OrmDBVersion(value=self.version)).\
                commit()

    def _run_migration(self, session: Session):
        """Runs migration flow. 
        If `version` != the database version run `_on_update` function.

        Args:
            session (Session): _description_
        """
        value = session.query(OrmDBVersion).first()

        if value.value != self.version:
            self._on_update(
                Migration(self.adapter, session),
                value.value,
                self.version,
            )
            session.update(OrmDBVersion, {'value': self.version}).\
                commit()

    @property
    def driver(self) -> str:
        """The driver name property"""
        return self._url.driver
