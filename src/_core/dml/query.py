from typing import Any, Dict, List, Tuple, TypeVar, Generic
from ..drivers.sql_adapter import SqlAdapter
from ..ddl.column import Column

_T = TypeVar('_T')


class Query(Generic[_T]):
    """Query object for creating queries and fetching result(s).

    Args:
        model_class(Model): The model for query. 
        Contain information about table.
        adapter: The SQL adapter for different drivers.
        session(Session): The session for executing query.
    """

    def __init__(
        self,
        model_class,
        adapter: SqlAdapter,
        session,
    ):
        self._model_class = model_class
        self._model = model_class()
        self._adapter = adapter
        self._session = session
        self._limit: int | None = None
        self._conditions: List[str] = []

    def _sql(self) -> str:
        """Creates SQL for query.

        Returns:
            str: SQL query.
        """
        adapter = self._adapter
        query = adapter.select(
            table=self._model.__tablename__,
            where=self._conditions,
            limit=self._limit,
        )

        return query

    def where(
        self,
        column: Column,
        value: Any,
        condition: str = '='
    ):
        """Adds WHERE condition to query.
        For getting row(s) use `first` or `all` method.

        Args:
            column: Condition column.
            value: Condition value.
            condition: Condition. For example: `=`, `LIKE`, `IN`.
            `=` by default.

        Returns:
            self: Query object for rows fetching.
        """
        value = column.type.insert_value(value, self._adapter)
        self._conditions.append(f'{column.name} {condition} {value}')
        return self

    def and_(
        self,
        column: Column,
        value: Any,
        condition: str = '='
    ):
        """Adds AND condition to query.
        Use `where` first!
        For getting row(s) use `first` or `all` method.

        Args:
            column: Condition column.
            value: Condition value.
            condition: Condition. For example: `=`, `LIKE`, `IN`.
            `=` by default.

        Returns:
            self: Query object for rows fetching.
        """
        value = column.type.insert_value(value, self._adapter)
        self._conditions.append(f'AND {column.name} {condition} {value}')
        return self

    def or_(
        self,
        column: Column,
        value: Any,
        condition: str = '='
    ):
        """Adds OR condition to query.
        Use `where` first!
        For getting row(s) use `first` or `all` method.

        Args:
            column: Condition column.
            value: Condition value.
            condition: Condition. For example: `=`, `LIKE`, `IN`.
            `=` by default.

        Returns:
            self: Query object for rows fetching.
        """
        value = column.type.insert_value(value, self._adapter)
        self._conditions.append(f'OR {column.name} {condition} {value}')
        return self

    def limit(self, limit: int):
        """Sets limit by rows to query.
        For getting row(s) use `first` or `all` method.

        Args:
            limit: Limit value.

        Returns:
            self: Query object for rows fetching.
        """
        self._limit = limit
        return self

    def first(self) -> _T | None:
        """Fetch the first row by query. None if not exist.

        Returns:
            _T | None: The first row by query. None if not exist.
        """
        if self._limit is None:
            self.limit(1)
        query = self._sql()
        one = self._session.fetch_one(query)

        return self._tuple_to_model(one) if one is not None else None

    def all(self) -> List[_T]:
        """Fetch all table rows by query.

        Returns:
            List[_T]: All table rows by query
        """
        query = self._sql()
        all = self._session.fetch_all(query)
        return [self._tuple_to_model(one) for one in all]

    def _tuple_to_model(self, result: Tuple[Any]) -> _T:
        """Convert tuple - database response to Model.

        Args:
            result: database response.

        Returns:
            _T: Model.
        """
        kwargs: Dict[str, Any] = {}
        for i, item in enumerate(result):
            kwargs[self._model.column_values.columns[i].field_name] = item
        return self._model_class(**kwargs)
