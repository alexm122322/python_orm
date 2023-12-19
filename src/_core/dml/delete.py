from typing import Any
from ..drivers.sql_adapter import SqlAdapter
from ..ddl.column import Column


class Delete:
    """Delete object for creating and executing deleting stmps.

    Args:
        model_class(Model): The model for stmp. 
        Contain information about table.
        adapter: The SQL adapter for different stmp.
        session(Session): The session for executing stmp.
    """

    def __init__(self, model, adapter: SqlAdapter, session):
        self._adapter = adapter
        self._session = session
        self._model = model
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
        """Executes DELETE stmp"""
        model = self._model()
        stmp = self._adapter.delete(model.__tablename__, self._conditions)
        self._session.execute(stmp)
        self._session.commit()
