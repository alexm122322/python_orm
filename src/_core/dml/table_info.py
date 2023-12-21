
from dataclasses import dataclass
from typing import Any, List

from ..drivers.sql_adapter import SqlAdapter
from ..schemas import ColumnInfo, ConstrainsInfo


class TableInfo:
    """TableInfo object for getting informtion about table.

    Args:
        model_class(Model): The model for stmp. 
        Contain information about table.
        adapter: The SQL adapter for different drivers.
        session(Session): The session for executing queries.
    """

    def __init__(self, model, adapter: SqlAdapter, session):
        self.model = model
        self._adapter = adapter
        self._session = session

    def columns_info(self) -> List[ColumnInfo]:
        """Fetches information about table columns.

        Return:
            List[ColumnInfo]: The columns information.
        """
        sql = self._adapter.table_columns_info(self.model.tn())
        rows = self._session.fetch_all(sql)
        infos = []
        for row in rows:
            info = self._adapter.columns_info_row_to_column_info(row)
            infos.append(info)
        return infos

    def constrains_info(self) -> List[ConstrainsInfo]:
        """Fetches information about table constraints.

        Return:
            List[ColumnInfo]: The constraints information.
        """
        sql = self._adapter.table_constraints_info(self.model.tn())
        rows = self._session.fetch_all(sql)
        infos = []
        for row in rows:
            info = self._adapter.constrains_info_row_to_constrains_info(
                row, self.model.tn())
            infos.append(info)
        return infos
