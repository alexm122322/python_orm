from src.orm import Session
from tests.conftest import User
from tests.init_funcs import insert_all, delete_all


def test_query_all(db_session: Session):
    insert_all(db_session)
    users = db_session.query(User).all()
    assert len(users) == 3
    delete_all(db_session)


def test_query_first(db_session: Session):
    insert_all(db_session)
    user = db_session.query(User).first()
    assert user is not None
    delete_all(db_session)


def test_query_where_all(db_session: Session):
    insert_all(db_session)
    users = db_session.query(User).\
        where(User.email, 'alexm1@str.com').\
        all()
    assert len(users) == 1

    users = db_session.query(User).\
        where(User.is_admin, True).\
        all()
    assert len(users) == 2

    users = db_session.query(User).\
        where(User.is_admin, False).\
        all()
    assert len(users) == 1

    delete_all(db_session)


def test_query_where_and_all(db_session: Session):
    insert_all(db_session)

    users = db_session.query(User).\
        where(User.is_admin, True).\
        and_(User.email, 'alexm1@str.com').\
        all()
    assert len(users) == 1

    delete_all(db_session)
