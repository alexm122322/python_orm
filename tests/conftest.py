from typing import Generator
from src.orm import Engine, DbUrl, create_session
import pytest


from src.orm import (Model, Column, IntegerColumnType, PrimaryKeyColumnType,
                     ForeignKey, DatetimeColumnType, BooleanColumnType, StringColumnType, datetime_now)


class User(Model):
    __tablename__ = 'user'

    id = Column(name='id', type=PrimaryKeyColumnType(
        type=IntegerColumnType(), autoincrement=True), unique=True)
    email = Column(name='email', type=StringColumnType(),
                   nullable=False, unique=True)
    age = Column(name='age', type=IntegerColumnType(default=18))
    is_admin = Column(name='is_admin', type=BooleanColumnType(default=True))
    create_at = Column(name='create_at', type=DatetimeColumnType(
        default=datetime_now))


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

    id = Column(name='id', type=PrimaryKeyColumnType(
        type=IntegerColumnType()), unique=True, nullable=False)
    user_id = Column(name='user_id', type=IntegerColumnType(),
                     unique=True, nullable=False)
    is_active = Column(name='is_active', type=BooleanColumnType(default=True))


@pytest.fixture(scope='session')
def db_session(request) -> Generator:
    url = DbUrl(
        driver='sqlite3',
        database='tests/test.sqlite3',
    )

    def on_create(create_tables):
        create_tables([User, Project])

    engine = Engine(db_url=url, on_create=on_create)
    session = create_session(engine)
    session.connect()
    try:
        yield session
    finally:
        session.disconnect()
        engine.drop_all_tables()
        engine.disconnect()
