
from src.orm import Session
from tests.conftest import User
from tests.init_funcs import delete_all, insert_all


def test_update_all(db_session: Session):
    insert_all(db_session)
    db_session.update(User, {'age': 25}).\
        commit()
    users = db_session.query(User).all()
    for user in users:
        assert user.age == 25
    delete_all(db_session)


def test_update_where(db_session: Session):
    insert_all(db_session)
    db_session.update(User, {'age': 25}).\
        where(User.email, 'alexm1@str.com').\
        commit()
    users = db_session.query(User).all()
    for user in users:
        if user.email == 'alexm1@str.com':
            assert user.age == 25
        else:
            assert user.age != 25
    delete_all(db_session)
