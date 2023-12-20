from src.orm import Migration, DbUrl, Engine, Model, Column, IntegerColumnType, StringColumnType


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
    value = Column(name='value', type=IntegerColumnType(), nullable=False)


def init_engine() -> Engine:
    engine = Engine(db_url=url)
    engine.create_tables([Test])
    engine.disconnect()
    return engine


def on_create(create_tables):
    pass


def migrate(migration: Migration, old_version: int, current_version: int):
    pass


def test_on_create_called(mocker):
    mock = mocker.patch(f'{__name__}.{on_create.__name__}')
    engine = Engine(url, 1, on_create=on_create)
    mock.assert_called_once()
    engine.disconnect()


def test_migration_called(mocker):
    mock = mocker.patch(f'{__name__}.{migrate.__name__}')
    init_engine()
    engine = Engine(url, 1, on_update=migrate)
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
        migration.add_column('test', Column(
            name='value2', type=StringColumnType()))
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
        value = Column(name='value', type=IntegerColumnType())

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
        value = Column(name='value', type=IntegerColumnType())

    def migrate(migration: Migration, old_version: int, current_version: int):
        migration.delete_table('test')
        tables = migration.table_list()
        assert not tables.__contains__('test')

    engine = Engine(url, 1, migrate)

    engine.drop_all_tables()
    engine.disconnect()
