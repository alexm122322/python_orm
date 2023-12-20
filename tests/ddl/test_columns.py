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


class IntegerTest(Model):
    __tablename__ = 'integer_test'
    value = Column(name='value', type=IntegerColumnType(), nullable=False)


class StringTest(Model):
    __tablename__ = 'string_test'
    value = Column(name='value', type=StringColumnType(
        len=1, default='s'), nullable=False)


class BooleanTest(Model):
    __tablename__ = 'boolean_test'
    value = Column(name='value', type=BooleanColumnType(), nullable=True)


class DatetimeTest(Model):
    __tablename__ = 'datetime_test'
    value = Column(name='value', type=DatetimeColumnType(), nullable=True)


def test_integer_columns():
    with create_session(engine) as session:
        migration = Migration(engine.adapter, session)
        migration.create_table(IntegerTest)
        info = session.table_info(IntegerTest).columns_info()[0]
        assert info.column_name == 'value'
        assert info.column_default == None
        assert info.is_nullable == 'NO'
        assert info.data_type == 'integer'
        assert info.character_maximum_length == None
        migration.delete_table('integer_test')


def test_string_columns():
    with create_session(engine) as session:
        migration = Migration(engine.adapter, session)
        migration.create_table(StringTest)
        info = session.table_info(StringTest).columns_info()[0]
        assert info.column_name == 'value'
        assert info.column_default == "'s'::character varying"
        assert info.is_nullable == 'NO'
        assert info.data_type == 'character varying'
        assert info.character_maximum_length == 1
        migration.delete_table('string_test')
    engine.drop_all_tables()


def test_boolean_columns():
    with create_session(engine) as session:
        migration = Migration(engine.adapter, session)
        migration.create_table(BooleanTest)
        info = session.table_info(BooleanTest).columns_info()[0]
        assert info.column_name == 'value'
        assert info.column_default == None
        assert info.is_nullable == 'YES'
        assert info.data_type.lower() == engine.adapter.boolean_column.lower()
        assert info.character_maximum_length == None
        migration.delete_table('boolean_test')
    engine.drop_all_tables()


def test_datetime_columns():
    with create_session(engine) as session:
        migration = Migration(engine.adapter, session)
        migration.create_table(DatetimeTest)
        info = session.table_info(DatetimeTest).columns_info()[0]
        assert info.column_name == 'value'
        assert info.column_default == None
        assert info.is_nullable == 'YES'
        assert info.data_type == 'timestamp without time zone'
        assert info.character_maximum_length == None
        migration.delete_table('datetime_test')
    engine.drop_all_tables()
    engine.disconnect()
