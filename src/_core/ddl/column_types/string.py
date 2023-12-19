from .column_type import ColumnType
from ...drivers.sql_adapter import SqlAdapter


class StringColumnType(ColumnType):
    """ColumnType implementation for string.

    Args:
        default: The default str value.
    """

    def __init__(self, len: int = 255, default: str | None = None):
        super().__init__(str, default)
        self._len = len

    def _sql(self, adapter: SqlAdapter) -> str:
        return adapter.string_column(self._len)
