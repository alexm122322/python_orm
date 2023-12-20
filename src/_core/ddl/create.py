from typing import List
from .column import Column
from .foreign_key import ForeignKey
from ..drivers.sql_adapter import SqlAdapter


class CreateTable:
    """CreateTable object for creating and executing migration ddl query.

    Args:
        adapter: The SQL adapter for different stmp.
        session(Session): The session for executing stmp.
    """

    def __init__(self, adapter: SqlAdapter, session):
        self._adapter = adapter
        self._session = session

    def create(self, model):
        """Creates table by a table tamplate. 
        No need `Session`.commit() after.

        Args:
            model (Model): The table tamplate.
        """
        columns: List[Column] = model.c()
        fkeys: List[ForeignKey] = model.fkeys()
        column_sqls = [column.sql(self._adapter) for column in columns]

        query = self._adapter.create_table(
            model.tn(),
            column_sqls,
            True,
            [fkey.sql(self._adapter) for fkey in fkeys],
        )
        self._session.execute(query)
        self._session.commit()
