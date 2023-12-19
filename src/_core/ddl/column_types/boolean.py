from .column_type import ColumnType
from ...drivers.sql_adapter import SqlAdapter


class BOOLEAN(ColumnType):
    """ColumnType implementation for Boolean.

    Args:
        default: The default bool value.
    """

    def __init__(self, default: bool | None = None):
        super().__init__(bool, default)

    def _sql(self, adapter: SqlAdapter) -> str:
        return adapter.boolean_column
