from ..sql_adapter import Psycopg2SqlAdapter


def datetime_now() -> str:
    """Psycopg2 `datetime_now` implementation.
    
    Returns:
        str: SQL for Psycopg2 `now` function.
    """
    adapter = Psycopg2SqlAdapter()
    return adapter.datetime_now