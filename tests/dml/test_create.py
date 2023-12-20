from src.orm import Engine, DbUrl, create_session, Model, Column, IntegerColumnType, PrimaryKeyColumnType, ForeignKey

db_url = DbUrl(
    driver='psycopg2',
    host='localhost',
    database='test1',
    user='postgres',
    password='1234',
    port='5432',
)

class Test1(Model):
    __tablename__ = 'test1'
    id = Column(name='id', type=PrimaryKeyColumnType(
        type=IntegerColumnType(), autoincrement=True))


class Test2(Model):
    __tablename__ = 'test2'
    id = Column(name='id', type=PrimaryKeyColumnType(
        type=IntegerColumnType(), autoincrement=True))
    test1_id = Column(
        name='test1_id', type=IntegerColumnType(), nullable=False)

    __foreignkey__ = ForeignKey(
        name='fk_test1',
        key_column='test1_id',
        parent_table='test1',
        parent_key_columns='id'
    )


class Test3(Model):
    __tablename__ = 'test3'
    id = Column(name='id', type=PrimaryKeyColumnType(
        type=IntegerColumnType(), autoincrement=True))
    test1_id = Column(
        name='test1_id', type=IntegerColumnType(), nullable=False)
    test2_id = Column(
        name='test2_id', type=IntegerColumnType(), nullable=False)

    __foreignkey_test1__ = ForeignKey(
        name='fk_test1',
        key_column='test1_id',
        parent_table='test1',
        parent_key_columns='id'
    )

    __foreignkey_test2__ = ForeignKey(
        name='fk_test2',
        key_column='test2_id',
        parent_table='test2',
        parent_key_columns='id'
    )


def test_create_with_one_f_keys():

    engine = Engine(db_url)
    engine.create_tables([Test1, Test2])
    with create_session(engine) as session:
        infos = session.table_info(Test2).constrains_info()
        target_info = None
        for info in infos:
            if info.constraint_name == 'fk_test1':
               target_info = info
        assert target_info is not None
        assert target_info.column_name == 'test1_id'
        assert target_info.foreign_table_name == 'test1'
        assert target_info.foreign_column_name == 'id'
    engine.drop_all_tables()
    engine.disconnect()


def test_create_with_few_f_keys():
    engine = Engine(db_url)
    engine.create_tables([Test1, Test2, Test3])
    with create_session(engine) as session:
        infos = session.table_info(Test3).constrains_info()
        target_info1 = None
        target_info2 = None
        for info in infos:
            if info.constraint_name == 'fk_test1':
               target_info1 = info
            elif info.constraint_name == 'fk_test2':
               target_info2 = info
        assert target_info1 is not None
        assert target_info1.column_name == 'test1_id'
        assert target_info1.foreign_table_name == 'test1'
        assert target_info1.foreign_column_name == 'id'
        
        assert target_info2 is not None
        assert target_info2.column_name == 'test2_id'
        assert target_info2.foreign_table_name == 'test2'
        assert target_info2.foreign_column_name == 'id'
    engine.drop_all_tables()
    engine.disconnect()
