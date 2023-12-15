from typing import Generator
from src.orm import Engine, Url, create_session
import pytest


from src.orm import Model, Column, Integer, PrimaryKey, ForeignKey, DATETIME, psycopg2_datetime_now, BOOLEAN, String


class User(Model):
    __tablename__ = '"user"'

    id = Column(name='id', type=PrimaryKey(
        type=Integer(), autoincrement=True), unique=True)
    email = Column(name='email', type=String(), nullable=False, unique=True)
    age = Column(name='age', type=Integer(default=18))
    is_admin = Column(name='is_admin', type=BOOLEAN(default=True))
    create_at = Column(name='create_at', type=DATETIME(default=psycopg2_datetime_now))


class Project(Model):
    __tablename__ = 'project'
    __foreignkey__ = ForeignKey(
        name='fk_user',
        key_column='user_id',
        parent_table='"user"',
        parent_key_columns='id',
        ondelete='CASCADE',
        onupdate='CASCADE',
    )

    id = Column(name='id', type=PrimaryKey(
        type=Integer()), unique=True, nullable=False)
    user_id = Column(name='user_id', type=Integer(),
                     unique=True, nullable=False)
    is_active = Column(name='is_active', type=BOOLEAN(default=True))


@pytest.fixture(scope='session')
def db_session(request) -> Generator:
    url = Url(
        driver='psycopg2',
        host='localhost',
        database='test',
        user='postgres',
        password='1234',
        port='5432',
    )
    engine = Engine(url=url)
    # engine.create_all_tables()

    session = create_session(engine)
    session.connect()
    try:
        yield session
    finally:
        session.disconnect()
        engine.drop_all_tables()
        engine.disconnect()


# next tasks:
#     5. test creating table(different column types)