from dataclasses import dataclass
from typing import Any
from .column_types.column_type import ColumnType
from ..drivers.sql_adapter import SqlAdapter


@dataclass
class Column:
    """The Column description.

    Returns:
        name: The name of the column.
        type: The type of the column.
        unique: Mark if column is unique. False by default.
        nullable: Mark if column is nullable. True by default.
    """
    name: str
    type: ColumnType
    unique: bool = False
    nullable: bool = True

    def sql(self, adapter: SqlAdapter) -> str:
        """SQL part of the column description.

        Args:
            adapter: The SQL adapter.

        Returns:
            str: SQL part of the column description.
        """
        unique = f' {adapter.unique}' if self.unique else ''
        nullable = f' {adapter.not_} {adapter.null}' if not self.nullable else ''
        type = f' {self.type.sql(adapter)}'
        return f'{self.name}{type}{unique}{nullable}'

    def insert_value(self, value: Any, adapter: SqlAdapter) -> str:
        """Adapt any value to SQL. 

        Args:
            value: The adapting value.
            adapter: The SQL adapter.

        Returns:
            str: Value for SQL.

        Raises:
            ValueError: The value is invalid.
        """
        return self.type.insert_value(value, adapter)
