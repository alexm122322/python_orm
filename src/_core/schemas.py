from dataclasses import dataclass
from typing import Any


@dataclass
class ColumnInfo:
    """Column info data class.

    Args:
        column_name: The name of the column.
        column_default: The default value of the column.
        is_nullable: Boolean value. If the collumn is nullable then true.
        data_type: The data type of the column.
        character_maximum_length: The character maximum lenght of the column.
    """
    column_name: str
    column_default: Any
    is_nullable: bool
    data_type: str
    character_maximum_length: int | None


@dataclass
class ConstrainsInfo:
    """Constrains info data class.

    Args:
        table_schema: The table schema name.
        constraint_name: The constraint name.
        table_name: The table name.
        column_name: The column name.
        foreign_table_schema: The foreign table schema name.
        foreign_table_name: The foreign table name.
        foreign_column_name: The foreign column name.
    """
    table_schema: str | None
    constraint_name: str | None
    table_name: str
    column_name: str
    foreign_table_schema: str
    foreign_table_name: str
    foreign_column_name: str
