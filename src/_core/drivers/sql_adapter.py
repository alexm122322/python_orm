from abc import ABC
from datetime import datetime
from typing import Any, Dict, List
from types import FunctionType

_create_teble_query = '''CREATE TABLE {if_not_exist}{name}(
    {columns}{foreign_key}
);'''

_foreign_key = '''
    CONSTRAINT {name}
        FOREIGN KEY({key_column})
            REFERENCES {parent_table}({parent_key_columns})'''


class SqlAdapter(ABC):
    """Class for adapting SQL language for different relative databases.
    The class contains basic realization for Postgresql. 
    Childs should override some methods for specific SQL drivers."""

    def string_column(self, len: int) -> str:
        return f'VARCHAR({len})'

    @property
    def integer_column(self) -> str:
        return f'INT'

    @property
    def boolean_column(self) -> str:
        return f'BOOLEAN'

    @property
    def timestamp_column(self) -> str:
        return f'timestamp'

    @property
    def autoincrement(self) -> str:
        return 'SERIAL'

    @property
    def autoincrement_default(self) -> str:
        return 'DEFAULT'

    @property
    def primary_key(self) -> str:
        return f'PRIMARY KEY'

    @property
    def not_(self) -> str:
        return f'NOT'

    @property
    def null(self) -> str:
        return f'NULL'

    @property
    def default(self) -> str:
        return f'DEFAULT'

    @property
    def unique(self) -> str:
        return f'UNIQUE'

    @property
    def if_not_exist(self) -> str:
        return f'IF NOT EXISTS'

    def boolean(self, value: bool) -> str:
        return "'t'" if value else "'f'"

    def any_value(self, value: Any) -> str:
        if isinstance(value, FunctionType):
            return value.__call__()
        elif isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, bool):
            return self.boolean(value)
        elif isinstance(value, datetime):
            return f"'{value}'"
        elif value is None:
            return self.null

        return f'{value}'

    def foreign_key(self, name: str, key_column: str, parent_table: str,
                    parent_key_columns: str, ondelete: str | None = None,
                    onupdate: str | None = None) -> str:
        sql = _foreign_key.format(
            name=name,
            key_column=key_column,
            parent_table=parent_table,
            parent_key_columns=parent_key_columns
        )

        if ondelete is not None:
            sql += f'''
            ON DELETE {ondelete}'''
        if onupdate is not None:
            sql += f'''
            ON UPDATE {onupdate}'''
        return sql

    def create_table(self, name: str, column_sqls: List[str],
                     if_not_exist: bool = False,
                     foreign_keys: List[str] = []) -> str:
        foreign_keys_sql = ',\n    '.join([i for i in foreign_keys])
        if foreign_keys:
            foreign_keys_sql = f',{foreign_keys_sql}'
        columns = ',\n    '.join([i for i in column_sqls])
        if_not_exist_sql = f'{self.if_not_exist} ' if if_not_exist else ''

        return _create_teble_query.format(
            name=name,
            columns=columns,
            if_not_exist=if_not_exist_sql,
            foreign_key=foreign_keys_sql,
        )

    @property
    def datetime_now(self) -> str:
        return f'now()'

    def select(self, table: str, columns: List[str] | None = None,
               limit: int | None = None, where: List[str] | None = None) -> str:
        columns = ',\n    '.join(columns) if columns is not None else '*'
        sql = f'''SELECT {columns} FROM {table}'''

        if where is not None and where:
            sql += ' WHERE '
            sql += ' '.join(where)
        if limit is not None:
            sql += f' {self.limit(limit)}'
        sql += ';'
        return sql

    def limit(self, limit: int) -> str:
        return f'LIMIT {limit}'

    @property
    def clear_database(self) -> str:
        return '''DROP SCHEMA public CASCADE;
CREATE SCHEMA public; 
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;'''

    def insert_items(self, table: str, columns: List[str],
                     list_values: List[List[Any]],
                     id_column: str | None = None) -> str:
        columns_str = ', '.join(columns)
        values_str_list = []
        returing = f'\nRETURNING {id_column}' if id_column is not None else ''

        for values in list_values:
            values_str_list.append(','.join(values))

        values_str = ', \n('.join([value + ')' for value in values_str_list])
        return f'''INSERT INTO {table}({columns_str})
VALUES ({values_str}{returing};'''

    def delete(self, tablename: str, conditions: List[str]) -> str:
        condition_str = ''
        if conditions:
            condition_str = '\nWHERE '
            condition_str += '\n'.join(conditions)
        return f'DELETE FROM {tablename}{condition_str};'

    def update(self, tablename: str, conditions: List[str],
               name_value: Dict[str, str]) -> str:
        condition_str = ''

        if conditions:
            condition_str = '\nWHERE '
            condition_str += '\n'.join(conditions)

        name_value_str = ' SET '
        name_value_str += '\n'.join([f'{name} = {item}'for name,
                                    item in name_value.items()])
        return f'''UPDATE {tablename}{name_value_str}{condition_str};'''

    @property
    def table_list(self) -> str:
        return "SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE';"

    def table_columns(self, tablename: str) -> str:
        return f'''SELECT column_name
FROM information_schema.columns
    WHERE table_schema = 'public'
    AND table_name = '{tablename}';'''

    def table_columns_info(self, tablename: str) -> str:
        """Utils sql query for getting info about Table.
        Return next columns: column_name, column_default, 
        is_nullable,data_type, character_maximum_length.

        Args:
            tablename: The name of the table.

        Returns:
            str: SQL query.
        """
        return f'''SELECT 
column_name,
column_default, 
is_nullable,
data_type,
character_maximum_length
FROM information_schema.columns
    WHERE table_schema = 'public'
    AND table_name = '{tablename}';'''

    def rename_table(self, old_name: str, new_name: str) -> str:
        return f'''{self._alter_table(old_name)}
    RENAME TO {new_name};'''

    def add_column(self, tablename: str, column: str) -> str:
        return f'''{self._alter_table(tablename)}
    ADD COLUMN {column};'''

    def drop_column(self, tablename: str, column_name: str) -> str:
        return f'''{self._alter_table(tablename)}
    DROP COLUMN {column_name}'''

    def drop_table(self, tablename: str):
        return f'DROP TABLE IF EXISTS {tablename};'

    def _alter_table(self, table_name: str) -> str:
        return f'ALTER TABLE {table_name}'

    def table_constraints_info(self, tablename: str) -> str:
        return f'''SELECT
    tc.table_schema as ts, 
    tc.constraint_name as cn, 
    tc.table_name as tn, 
    kcu.column_name as kn, 
    ccu.table_schema AS foreign_table_schema,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.table_schema='public'
    AND tc.table_name='{tablename}'	
    GROUP BY ts, cn, tn, kn, foreign_table_schema, foreign_table_name, foreign_column_name;'''
