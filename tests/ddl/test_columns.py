from src.orm import (Url, Model, Column, Integer,
                     Engine, create_session, String, Migration, BOOLEAN, DATETIME)

url = Url(
    driver='psycopg2',
    host='localhost',
    database='test1',
    user='postgres',
    password='1234',
    port='5432',
)

engine = Engine(url=url)


def test_integer_columns():
    class Test(Model):
        __tablename__ = 'test'
        value = Column(name='value', type=Integer(), nullable=False)

    with create_session(engine) as session:
        migration = Migration(engine.adapter, session)
        migration.create_table(Test)
        info = session.fetch_one(engine.adapter.table_columns_info('test'))
        assert info[0] == 'value'
        assert info[1] == None
        assert info[2] == 'NO'
        assert info[3] == 'integer'
        assert info[4] == None
        migration.delete_table('test')


def test_string_columns():
    class Test(Model):
        __tablename__ = 'test'
        value = Column(name='value', type=String(
            len=1, default='s'), nullable=False)

    with create_session(engine) as session:
        migration = Migration(engine.adapter, session)
        migration.create_table(Test)
        info = session.fetch_one(engine.adapter.table_columns_info('test'))
        assert info[0] == 'value'
        assert info[1] == "'s'::character varying"
        assert info[2] == 'NO'
        assert info[3] == 'character varying'
        assert info[4] == 1
        migration.delete_table('test')
    engine.drop_all_tables()


def test_boolean_columns():
    class Test(Model):
        __tablename__ = 'test'
        value = Column(name='value', type=BOOLEAN(), nullable=True)

    with create_session(engine) as session:
        migration = Migration(engine.adapter, session)
        migration.create_table(Test)
        info = session.fetch_one(engine.adapter.table_columns_info('test'))
        assert info[0] == 'value'
        assert info[1] == None
        assert info[2] == 'YES'
        assert info[3].lower() == engine.adapter.boolean_column.lower()
        assert info[4] == None
        migration.delete_table('test')
    engine.drop_all_tables()


def test_datetime_columns():
    class Test(Model):
        __tablename__ = 'test'
        value = Column(name='value', type=DATETIME(), nullable=True)

    with create_session(engine) as session:
        migration = Migration(engine.adapter, session)
        migration.create_table(Test)
        info = session.fetch_one(engine.adapter.table_columns_info('test'))
        assert info[0] == 'value'
        assert info[1] == None
        assert info[2] == 'YES'
        assert info[3] == 'timestamp without time zone'
        assert info[4] == None
        migration.delete_table('test')
    engine.drop_all_tables()
    engine.disconnect()
