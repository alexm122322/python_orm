from typing import List
from .errors import DifferentModelsTypeError
from ..ddl.model import Model
from ..drivers.sql_adapter import SqlAdapter


class Insert:
    """Object which respond for inserting models.

    Args:
        adapter: The Sql adapter.
        session: The session for running stmps.
    """

    def __init__(self, adapter: SqlAdapter, session):
        self._adpter = adapter
        self._session = session
        self._items: List[Model] = []

    def commit(self) -> List[int] | None:
        """Commit Model(s) adding.

        Args:
            item: Adding item.

        Returns:
           List [int] | None: Id of adding item. None if column_id is not exist.

        Raises:
            DifferentModelsTypeError: if items are different models.
        """
        if not self._items:
            return

        etalon = self._items[0]
        etalon_type = type(etalon)
        for model in self._items:
            if not isinstance(model, etalon_type):

                raise DifferentModelsTypeError(
                    f'All models should be {etalon_type} type.')

        sql = self._adpter.insert_items(
            table=etalon.__tablename__,
            columns=[c.column_name for c in etalon.column_values.columns],
            id_column=etalon.table_id.name if etalon.table_id is not None else None,
            list_values=[[c.insert_value(self._adpter) for c in item.column_values.columns]
                         for item in self._items],
        )
        ids = None
        if etalon.table_id is not None:
            ids = self._session.fetch_all(sql)
        else:
            self._session.execute(sql)
        self._session.commit()

        return [id[0] for id in ids] if ids else None

    def add_item(self, item: Model):
        """Add Item to Model Table.

        Args:
            item: Adding item.

        Returns:
            self: current Insert object.
        """
        self._items.append(item)
        return self

    def add_items(self, items: List[Model]):
        """Add Items to Model Table.

        Args:
            items: Adding items.

        Returns:
            self: current Insert object.

        """
        self._items.extend(items)
        return self
