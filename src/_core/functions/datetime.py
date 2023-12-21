from ..drivers.sql_adapter import SqlAdapter


def datetime_now(adapter: SqlAdapter) -> str:
    """Psycopg2 `datetime_now` implementation.

    Returns:
        str: SQL for Psycopg2 `now` function.
    """
    return adapter.datetime_now
