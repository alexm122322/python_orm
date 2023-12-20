
from dataclasses import dataclass
from typing import Any, List

from ..drivers.sql_adapter import SqlAdapter


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
    is_nullable: str
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
    table_schema: str
    constraint_name: str
    table_name: str
    column_name: str
    foreign_table_schema: str
    foreign_table_name: str
    foreign_column_name: str


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
            info = ColumnInfo(
                column_name=row[0],
                column_default=row[1],
                is_nullable=row[2],
                data_type=row[3],
                character_maximum_length=row[4],
            )
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
            info = ConstrainsInfo(
                table_schema=row[0],
                constraint_name=row[1],
                table_name=row[2],
                column_name=row[3],
                foreign_table_schema=row[4],
                foreign_table_name=row[5],
                foreign_column_name=row[6],
            )
            infos.append(info)
        return infos
