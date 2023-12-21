from typing import List
from .column import Column
from ..drivers.sql_adapter import SqlAdapter
from .model import Model
from ..ddl.create import CreateTable


class Migration:
    """Migration object for creating and executing migration ddl queries.

    Args:
        adapter: The SQL adapter for different stmp.
        session(Session): The session for executing stmp.
    """

    def __init__(self, adapter: SqlAdapter, session):
        self._adapter = adapter
        self._session = session
        
    def table_list(self) -> List[str]:
        """Fetches a list of table names from Databse.

        Returns:
            List[str]: A List of table names.
        """
        sql = self._adapter.table_list
        names = self._session.fetch_all(sql)
        return [name[0] for name in names]

    def change_table_name(self, old_name: str, new_name: str):
        """Chnages name of table.

        Args:
            old_name: The name of the table that changes.
            new_name: The new name of the table.
        """
        sql = self._adapter.rename_table(old_name, new_name)
        self._session.execute(sql)
        self._session.commit()

    def add_column(self, tablename: str, column: Column):
        """Addes column to table.

        Args:
            tablename: The table name which will be a column added.
            column: The column which will be added.
        """
        sql = self._adapter.add_column(tablename, column.sql(self._adapter))
        self._session.execute(sql)
        self._session.commit()

    def delete_column(self, tablename: str, column_name: str):
        """Deletes column from the table.

        Args:
            tablename: The table name which will be a column deleted.
            column: The column which will be deleted.
        """
        sql = self._adapter.drop_column(tablename, column_name)
        self._session.execute(sql)
        self._session.commit()

    def create_table(self, table: Model):
        """Creates table.

        Args:
            table (Model): The tamplate of the table.
        """
        create_table = CreateTable(self._adapter, self._session)
        create_table.create(table)

    def delete_table(self, tablename: str):
        """Delete table if exist.

        Args:
            tablename: The table name. 
        """
        sql = self._adapter.drop_table(tablename)
        self._session.execute(sql)
        self._session.commit()
