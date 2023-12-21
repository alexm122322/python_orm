from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List
from ..errors import ValueError

from ...drivers.sql_adapter import SqlAdapter


class ColumnType(ABC):
    """The abstract of ColumnType.

    Args:
        type(Type): The type of the column. For Example datetime, str, bool, int.
        default: The default value of the column.
    """

    def __init__(self, type, default: Any | None = None):
        self.type = type
        self.default = default

    def validate_value(self, value: Any) -> bool:
        """Validates the value.

        Args:
            value: The validation value.

        Returns:
            bool: True if value is valid. False if not.
        """
        if isinstance(self.type, List):
            for t in self.type:
                if isinstance(value, t):
                    return True
            return False
        return isinstance(value, self.type)
    
    def fix_value(self, value: Any) -> Any:
        """Fixes value if needed. For example int to bool purposes.
        See the `Column Type` implementations for details.
        
        Args:
            value: Any column value.
            
        Return:
            Any: Fixed value.
        """
        return value

    @abstractmethod
    def _sql(self, adapter: SqlAdapter) -> str:
        """Creates SQL of column type. For example VARCHAR
        Should be implemented by childs.

        Args:
            adapter: The SQL adapter.

        Returns:
            str: The SQL of column.
        """
        pass

    def insert_value(self, value: Any, adapter: SqlAdapter) -> str:
        if value is not None and not self.validate_value(value):
            raise ValueError(
                f'Value {value}{type(value)} for column({self}) is not valid.')
        return adapter.any_value(value)

    def sql(self, adapter: SqlAdapter) -> str:
        """Creates SQL of column.

        Args:
            adapter: The SQL adapter.

        Returns:
            str: The SQL of column.
        """
        sql = self._sql(adapter)
        sql = self._default_wrap(sql, adapter)
        return sql

    def _default_wrap(self, sql: str, adapter: SqlAdapter) -> str:
        """Wrap `sql` with default value.

        Args:
            sql: The SQL of column.
            adapter: The SQL adapter.

        Returns:
            str: Wrapped column SQL. 
             Return original `sql` if default is None.
        """
        if self.default is None:
            return sql

        return f'{sql} {adapter.default} {adapter.any_value(self.default)}'
