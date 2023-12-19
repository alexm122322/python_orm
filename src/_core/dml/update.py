from typing import Any, Dict, List
from ..drivers.sql_adapter import SqlAdapter
from ..ddl.column import Column


class Update:
    """Update object for creating and executing updatinging stmps.

    Args:
        model_class(Model): The model for stmp. 
        Contain information about table.
        adapter: The SQL adapter for different drivers.
        session(Session): The session for executing stmp.
        name_value: Name value mapping for SET in UPDATE stmp.
    """

    def __init__(self, model, adapter: SqlAdapter, session,
                 name_value: Dict[str, str]):
        self._adapter = adapter
        self._session = session
        self._model = model
        self._name_value = name_value
        self._conditions = []

    def where(self, column: Column, value: Any, condition: str = '='):
        """Adds WHERE condition to stmp.
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

    def and_(self, column: Column, value: Any, condition: str = '='):
        """Adds AND condition to stmp.
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

    def or_(self, column: Column, value: Any, condition: str = '='):
        """Adds OR condition to stmp.
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

    def commit(self):
        """Executes UPDATE stmp"""

        model = self._model()
        stmp = self._adapter.update(
            model.__tablename__,
            self._conditions,
            self._name_value,
        )
        self._session.execute(stmp)
        self._session.commit()
