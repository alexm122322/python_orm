from logging import getLogger
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

from .dml.query import Query
from .dml.insert import Insert
from .dml.delete import Delete
from .dml.update import Update
from .drivers.sql_adapter import SqlAdapter
from .ddl.create import CreateTable

logger = getLogger(__name__)


class Session(ABC):
    """Session of the database.

    Args:
        connection: The connection to the database.
        adapter: The SQL adapter for queries.
    """

    def __init__(self,
                 connection: Any,
                 adapter: SqlAdapter
                 ):
        self.adapter = adapter
        self._connection = connection

    def __enter__(self):
        """Context Manage enter realization."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context Manage exit realization."""
        self.disconnect()

    @abstractmethod
    def connect(self):
        """Create session connection."""
        logger.info('connect')

    @abstractmethod
    def disconnect(self):
        """Disconnect session."""
        logger.info('disconnect')

    @abstractmethod
    def execute(self, sql: str):
        """Excute sql.

        Args:
            sql: The SQL which will be execute.
        """
        pass

    @abstractmethod
    def commit(self):
        """Commit any changes like insertion, deletion, updating."""
        pass

    @abstractmethod
    def fetch_one(
        self,
        sql: str,
    ) -> Tuple[Any] | None:
        """Fetch one result of sql.

        Args:
            sql: The SQL which will be execute.

        Returns:
            Tuple[Any] | None: Result of executing. None if result is empty.
        """
        pass

    @abstractmethod
    def fetch_all(
        self,
        sql: str,
    ) -> List[Tuple[Any]]:
        """Fetch all results of sql.

        Args:
            sql: The SQL which will be execute.

        Returns:
            List[Tuple[Any]]: Results of executing.
        """
        pass

    def query(self, model) -> Query:
        """Database query. 
        Query object contains the method for customization query like
        `limit`, `where`, `and_`, `or_`. For get result(s) call `first` 
        or `all` methods.


        Args:
            model(Model): Table model.

        Returns:
            Query: The query object. 
        """
        return Query(model, self.adapter, self)

    def insert_item(self, item) -> Insert:
        """Adds item to Model Table.
        To finish the transaction should call commit.

        Args:
            item(Model) : Adding item.

        Returns:
            Insert: Insert object for finish transaction by commit.
        """
        return Insert(self.adapter, self).add_item(item)

    def insert_items(self, items: List) -> Insert:
        """Adds items to Model Table. 
        To finish the transaction should call commit.

        Args:
            items(List[Model]) : Adding items.

        Returns:
            Insert: Insert object for finish transaction by commit.
        """
        return Insert(self.adapter, self).add_items(items)

    def delete(self, model) -> Delete:
        """Delete stmt. 
        Stmt object contains the method for customization stmt like
        `where`, `and_`, `or_`. For execute stmt call `commit` method.

        Args:
            model(Model): Table model.

        Returns:
            Delete: The delete object. 
        """
        return Delete(model, self.adapter, self)

    def update(self, model, name_value: Dict[str, str]) -> Update:
        """Update stmt. 
        Stmt object contains the method for customization stmt like
        `where`, `and_`, `or_`. For execute stmt call `commit` method.

        Args:
            model(Model): Table model.
            name_value: Name value mapping for SET in UPDATE stmt

        Returns:
            Delete: The delete object. 
        """
        return Update(model, self.adapter, self, name_value)

    def create_table(self, model) -> CreateTable:
        """Create table stmt. No need to call `commit`. 
        Creates a table instantly.

        Args:
            model(Model): Table model.

        Returns:
            CreateTable: The crete table object. 
        """
        return CreateTable(self.adapter, self).create(model)
