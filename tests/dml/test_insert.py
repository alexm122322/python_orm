from typing import List
from _core.dml.errors import DifferentModelsTypeError
from src.orm import Session
from tests.conftest import User, Project
from datetime import datetime
from tests.init_funcs import delete_all

def test_insert_item(db_session: Session):
    now = datetime.now()
    item = User(
        age=18,
        email='alexm@str.com',
        is_admin=True,
        create_at=now,
    )
    ids = db_session.insert_item(item).commit()
    result = db_session.query(User).all()
    assert len(result) == 1
    user = result[0]
    assert ids[0] == user.id
    assert user.age == 18
    assert user.email == 'alexm@str.com'
    assert user.is_admin
    assert user.create_at == now

    db_session.delete(User).commit()
    result = db_session.query(User).all()
    assert len(result) == 0


def test_insert_items(db_session: Session):
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

    ids = db_session.insert_items([item1, item2, item3]).commit()
    assert len(ids) == 3
    items: List[User] = db_session.query(User).all()
    assert len(items) == 3
    dict1 = item1.dict
    dict2 = item2.dict
    dict3 = item3.dict

    for item in items:
        if item.id == ids[0]:
            select_item1 = item
            dict1['id'] = ids[0]
        if item.id == ids[1]:
            select_item2 = item
            dict2['id'] = ids[1]
        if item.id == ids[2]:
            select_item3 = item
            dict3['id'] = ids[2]

    assert dict1 == select_item1.dict
    assert dict2 == select_item2.dict
    assert dict3 == select_item3.dict

    db_session.delete(User).commit()
    result = db_session.query(User).all()
    assert len(result) == 0


def test_insert_different_items(db_session: Session):
    """insert_items methods must raise DifferentModelsTypeError 
    if adding different models.
    """
    now = datetime.now()
    user = User(
        age=18,
        email='alexm1@str.com',
        is_admin=True,
        create_at=now,
    )
    user_id = db_session.insert_item(user).commit()[0]

    user1 = User(
        age=20,
        email='alexm2@str.com',
        is_admin=True,
        create_at=now,
    )
    project = Project(
        user_id=user_id,
        is_active=True,
    )
    try:
        user_id = db_session.insert_items([user1, project])
    except Exception as e:
        assert isinstance(e, DifferentModelsTypeError)
    
    delete_all(db_session)
