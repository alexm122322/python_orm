from datetime import datetime
from types import FunctionType
from typing import Any, List, Tuple

from ..sql_adapter import SqlAdapter
from ...schemas import ColumnInfo, ConstrainsInfo


class SqLite3SqlAdapter(SqlAdapter):
    """The specific implementation of SQL adapter for SQLite driver."""

    def __init__(self):
        self.create_unique: bool = True

    def string_column(self, len: int) -> str:
        return f'TEXT'

    @property
    def integer_column(self) -> str:
        return f'INTEGER'

    @property
    def boolean_column(self) -> str:
        return f'INTEGER'

    @property
    def timestamp_column(self) -> str:
        return f'TIMESTAMP'

    @property
    def datetime_now(self) -> str:
        return f'CURRENT_TIMESTAMP'

    @property
    def autoincrement(self) -> str:
        return ''

    @property
    def null(self) -> str:
        return f'NULL'

    def primary_column(self, sql_column: str, is_autoincremented: bool):
        return f'{sql_column} {self.primary_key}'

    @property
    def unique(self) -> str:
        return f''

    def boolean(self, value: bool) -> str:
        return '1' if value else '0'

    def any_value(self, value: Any) -> str:
        if isinstance(value, FunctionType):
            return value.__call__(self)
        elif isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, bool):
            return self.boolean(value)
        elif isinstance(value, datetime):
            return f"'{value}'"
        elif value is None:
            return self.null

        return f'{value}'

    @property
    def autoincrement_default(self) -> str:
        return 'NULL'

    @property
    def clear_database(self) -> List[str]:
        return [
            'PRAGMA writable_schema = 1;',
            "delete from sqlite_master where type in ('table', 'index', 'trigger');",
            'PRAGMA writable_schema = 0;',
        ]

    def table_columns(self, tablename: str) -> str:
        return f'''pragma table_info({tablename})'''

    def table_columns_info(self, tablename: str) -> str:
        """This pragma returns one row for each normal column in the named table. 
        Columns in the result set include: "name" (its name); "type" (data type if given, else ''); 
        "notnull" (whether or not the column can be NULL); 
        "dflt_value" (the default value for the column); 
        and "pk" (either zero for columns that are not part of the primary key, 
        or the 1-based index of the column within the primary key).

        Args:
            tablename: The name of the table.

        Returns:
            str: SQL query.
        """
        return f'''pragma table_info({tablename});'''

    def table_columns_info_to_column_info(self, row: Tuple) -> ColumnInfo:
        return ColumnInfo(
            column_name=row[1],
            column_default=row[4],
            is_nullable=True if row[3] == 0 else False,
            data_type=row[2],
            character_maximum_length=None,
        )

    def table_constraints_info(self, tablename: str) -> str:
        return f"pragma foreign_key_list({tablename});"

    def table_constrains_info_to_constrains_info(self, row: Tuple, tablename: str) -> ConstrainsInfo:
        return ConstrainsInfo(
            table_schema=None,
            constraint_name=None,
            table_name=tablename,
            column_name=row[3],
            foreign_table_schema=None,
            foreign_table_name=row[2],
            foreign_column_name=row[4],
        )
