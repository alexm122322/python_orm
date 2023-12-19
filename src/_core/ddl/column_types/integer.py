from .column_type import ColumnType
from ...drivers.sql_adapter import SqlAdapter


class IntegerColumnType(ColumnType):
    """ColumnType implementation for integer.

    Args:
        default: The default int value.
    """

    def __init__(self, default: int | None = None):
        super().__init__(int, default)

    def _sql(self, adapter: SqlAdapter) -> str:
        return adapter.integer_column
