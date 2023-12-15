from datetime import datetime
from src.orm import Session
from tests.conftest import User
from tests.init_funcs import insert_all, delete_all

def test_delete_all(db_session: Session):
    insert_all(db_session)
    delete_all(db_session)


def test_delete_where(db_session: Session):
    insert_all(db_session)

    db_session.delete(User).\
        where(User.email, 'alexm1@str.com').\
        commit()

    user = db_session.query(User).\
        where(User.email, 'alexm1@str.com').\
        first()
    assert user is None
    delete_all(db_session)


def test_delete_where_and(db_session: Session):
    insert_all(db_session)

    db_session.delete(User).\
        where(User.email, 'alexm1@str.com').\
        and_(User.age, 20).\
        commit()

    user = db_session.query(User).\
        where(User.email, 'alexm1@str.com').\
        first()
    assert user is not None

    db_session.delete(User).\
        where(User.email, 'alexm1@str.com').\
        and_(User.age, 18).\
        commit()

    user = db_session.query(User).\
        where(User.email, 'alexm1@str.com').\
        first()
    assert user is None
    delete_all(db_session)


def test_delete_where_or(db_session: Session):
    insert_all(db_session)

    db_session.delete(User).\
        where(User.email, 'alexm1@str.com').\
        or_(User.age, 20).\
        commit()

    users = db_session.query(User).\
        all()
    assert len(users) == 1
    delete_all(db_session)
