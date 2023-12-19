from datetime import datetime
from types import FunctionType
from typing import Any

from .column_type import ColumnType
from ...drivers.sql_adapter import SqlAdapter


class DATETIME(ColumnType):
    """ColumnType implementation for datetime.

    Args:
        default: The default function or str value.
    """

    def __init__(self, default: FunctionType | str | None = None):
        super().__init__(datetime, default)

    def _sql(self, adapter: SqlAdapter) -> str:
        return adapter.timestamp_column
