from src.orm import (DbUrl, Model, Column, IntegerColumnType,
                     Engine, create_session, StringColumnType, Migration, BooleanColumnType, DatetimeColumnType)

url = DbUrl(
    driver='psycopg2',
    host='localhost',
    database='test1',
    user='postgres',
    password='1234',
    port='5432',
)

engine = Engine(db_url=url)


def test_integer_columns():
    class Test(Model):
        __tablename__ = 'test'
        value = Column(name='value', type=IntegerColumnType(), nullable=False)

    with create_session(engine) as session:
        migration = Migration(engine.adapter, session)
        migration.create_table(Test)
        info = session.table_info(Test).columns_info()[0]
        assert info.column_name == 'value'
        assert info.column_default == None
        assert info.is_nullable == 'NO'
        assert info.data_type == 'integer'
        assert info.character_maximum_length == None
        migration.delete_table('test')


def test_string_columns():
    class Test(Model):
        __tablename__ = 'test'
        value = Column(name='value', type=StringColumnType(
            len=1, default='s'), nullable=False)

    with create_session(engine) as session:
        migration = Migration(engine.adapter, session)
        migration.create_table(Test)
        info = session.table_info(Test).columns_info()[0]
        assert info.column_name == 'value'
        assert info.column_default == "'s'::character varying"
        assert info.is_nullable == 'NO'
        assert info.data_type == 'character varying'
        assert info.character_maximum_length == 1
        migration.delete_table('test')
    engine.drop_all_tables()


def test_boolean_columns():
    class Test(Model):
        __tablename__ = 'test'
        value = Column(name='value', type=BooleanColumnType(), nullable=True)

    with create_session(engine) as session:
        migration = Migration(engine.adapter, session)
        migration.create_table(Test)
        info = session.table_info(Test).columns_info()[0]
        assert info.column_name == 'value'
        assert info.column_default == None
        assert info.is_nullable == 'YES'
        assert info.data_type.lower() == engine.adapter.boolean_column.lower()
        assert info.character_maximum_length == None
        migration.delete_table('test')
    engine.drop_all_tables()


def test_datetime_columns():
    class Test(Model):
        __tablename__ = 'test'
        value = Column(name='value', type=DatetimeColumnType(), nullable=True)

    with create_session(engine) as session:
        migration = Migration(engine.adapter, session)
        migration.create_table(Test)
        info = session.table_info(Test).columns_info()[0]
        assert info.column_name == 'value'
        assert info.column_default == None
        assert info.is_nullable == 'YES'
        assert info.data_type == 'timestamp without time zone'
        assert info.character_maximum_length == None
        migration.delete_table('test')
    engine.drop_all_tables()
    engine.disconnect()
