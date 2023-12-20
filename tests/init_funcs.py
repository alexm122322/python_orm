from datetime import datetime
from src.orm import Session
from tests.conftest import User


def insert_all(db_session: Session):
    now = datetime.now()
    item1 = User(
        age=18,
        email='alexm1@str.com',
        is_admin=True,
        create_at=now,
    )
    item2 = User(
        age=19,
        email='alexm2@str.com',
        is_admin=False,
        create_at=now,
    )
    item3 = User(
        age=20,
        email='alexm3@str.com',
        is_admin=True,
        create_at=now,
    )

    db_session.\
        insert_items([item1, item2, item3]).\
        commit()

    all = db_session.\
        query(User).\
        all()
    assert len(all) == 3


def delete_all(db_session: Session):
    db_session.\
        delete(User).\
        commit()
    all = db_session.query(User).all()
    assert len(all) == 0
