from typing import Any
from .column_type import ColumnType
from .integer import Integer
from ..errors import AutoincrementTypeError
from ...drivers.sql_adapter import SqlAdapter


class PrimaryKey(ColumnType):
    """ColumnType implementation for Primary Key.

    Args:
        type: The type of PrimaryKey.
        autoincrement: True if the Primary key should be auto-increment. 
        False by default. At the moment supports only `Integer`. 
    """
    _autoincrement_types = [Integer]

    def __init__(
        self,
        type: ColumnType,
        autoincrement: bool = False,
    ):
        super().__init__(None)
        self.type = type
        self.autoincrement = autoincrement

    def _sql(self, adapter: SqlAdapter) -> str:
        """Implementation of `ColumnType`._sql.

        Args:
            adapter: The SQL adapter.

        Returns:
            str: The SQL of column.

        Raises:
            AutoincremantTypeError: Auto increment type is not supported.
             Check out the `_autoincrement_types` - the list of 
             supported Auto increment types.
        """

        if self.autoincrement and not self._autoincrement_types.__contains__(type(self.type)):
            raise AutoincrementTypeError(
                f'Type for autoincrement Primary Key should be {self._autoincrement_types}')

        pk_type = adapter.autoincrement if self._is_autoincrement else self.type.sql(
            adapter)
        return f'{pk_type} {adapter.primary_key}'

    def validate_value(self, value: Any) -> bool:
        """Overriding of `ColumnType`.validate_value."""
        return self.type.validate_value(value)

    def insert_value(self, value: Any, adapter: SqlAdapter) -> str:
        """Overriding of `ColumnType`.insert_value."""
        if value is None and self._is_autoincrement:
            return adapter.autoincrement_default
        return adapter.any_value(value)

    @property
    def _is_autoincrement(self) -> bool:
        """Util property. Detect if value is auto-incremented.

        Returns:
            bool: True if 
        """
        if self.autoincrement:
            for type in self._autoincrement_types:
                if isinstance(self.type, type):
                    return True

        return False
