from ..drivers.sql_adapter import SqlAdapter


class ForeignKey:
    """Realization of the Foreign Key.

    Args:
        name: The name of the Foreign Key.
        key_column: The name of Foreign Key column.
        parent_table: The name of parent table.
        parent_key_columns: The name of parent table column.
        ondelete: The behavior of deleting. For example 'ON CASCADE'
        onupdate: The behavior of updating. For example 'ON CASCADE'
    """

    def __init__(
        self,
        name: str,
        key_column: str,
        parent_table: str,
        parent_key_columns: str,
        ondelete: str | None = None,
        onupdate: str | None = None,
    ):
        self._name = name
        self._key_column = key_column
        self._parent_table = parent_table
        self._parent_key_columns = parent_key_columns
        self._ondelete = ondelete
        self._onupdate = onupdate

    def sql(self, adapter: SqlAdapter,) -> str:
        """Creates SQL for the Foreign Key.

        Args:
            adapter: The SQL adapter.

        Returns:
            str: SQL of Foreign Key.
        """
        return adapter.foreign_key(
            name=self._name,
            key_column=self._key_column,
            parent_table=self._parent_table,
            parent_key_columns=self._parent_key_columns,
            ondelete=self._ondelete,
            onupdate=self._onupdate,
        )
