from typing import Any
from .column_type import ColumnType
from ...drivers.sql_adapter import SqlAdapter


class BooleanColumnType(ColumnType):
    """ColumnType implementation for Boolean.

    Args:
        default: The default bool value.
    """

    def __init__(self, default: bool | None = None):
        super().__init__([bool, int], default)

    def _sql(self, adapter: SqlAdapter) -> str:
        return adapter.boolean_column

    def fix_value(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        elif isinstance(value, int):
            return True if value == 1 else 0
        return value