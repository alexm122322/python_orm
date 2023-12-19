from src.orm import Migration, DbUrl, Engine, Model, Column, Integer, String


url = DbUrl(
    driver='psycopg2',
    host='localhost',
    database='test1',
    user='postgres',
    password='1234',
    port='5432',
)


class Test(Model):
    __tablename__ = 'test'
    value = Column(name='value', type=Integer(), nullable=False)


def init_engine() -> Engine:
    engine = Engine(url=url)
    engine.disconnect()
    return engine


def migrate(migration: Migration, old_version: int, current_version: int):
    pass


def test_migration_called(mocker):
    mock = mocker.patch(f'{__name__}.{migrate.__name__}')
    init_engine()
    engine = Engine(url, 1, migrate)
    mock.assert_called_once()
    engine.drop_all_tables()
    engine.disconnect()


def test_change_table_name():
    init_engine()

    def migrate(migration: Migration, old_version: int, current_version: int):
        migration.change_table_name('test', 'test1')
        tables = migration.table_list()
        assert tables.__contains__('test1')
        assert not tables.__contains__('test')
    engine = Engine(url, 1, migrate)

    engine.drop_all_tables()
    engine.disconnect()


def test_add_column():
    init_engine()

    def migrate(migration: Migration, old_version: int, current_version: int):
        migration.add_column('test', Column(name='value2', type=String()))
        columns = migration.table_columns('test')
        assert columns.__contains__('value2')
    engine = Engine(url, 1, migrate)

    engine.drop_all_tables()
    engine.disconnect()


def test_delete_column():
    init_engine()

    def migrate(migration: Migration, old_version: int, current_version: int):
        migration.delete_column('test', 'value')
        columns = migration.table_columns('test')
        assert not columns
    engine = Engine(url, 1, migrate)

    engine.drop_all_tables()
    engine.disconnect()


def test_add_table():
    init_engine()

    class Test2(Model):
        __tablename__ = 'test2'
        value = Column(name='value', type=Integer())

    def migrate(migration: Migration, old_version: int, current_version: int):
        migration.create_table(Test2)
        tables = migration.table_list()
        assert tables.__contains__('test2')
        columns = migration.table_columns('test')
        assert columns[0] == 'value'
    engine = Engine(url, 1, migrate)

    engine.drop_all_tables()
    engine.disconnect()


def test_drop_table():
    init_engine()

    class Test(Model):
        __tablename__ = 'test'
        value = Column(name='value', type=Integer())

    def migrate(migration: Migration, old_version: int, current_version: int):
        migration.delete_table('test')
        tables = migration.table_list()
        assert not tables.__contains__('test')

    engine = Engine(url, 1, migrate)

    engine.drop_all_tables()
    engine.disconnect()
