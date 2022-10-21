import pytest

import db.user_types as usr
from server.tests.test_endpoints import TEST_CLIENT


def test_get_users():
    usrs = usr.get_users()
    assert isinstance(usrs, list)
    assert len(usrs) > 1


def test_get_user_details():
    usr_dets = usr.get_user_type_details(usr.Investor)
    assert isinstance(usr_dets, list)


def test_add_wrong_name_type():
    with pytest.raises(TypeError):
        usr.add_user(7, {})


def test_add_wrong_details_type():
    with pytest.raises(TypeError):
        usr.add_user('a new user', [])


def test_add_missing_field():
    with pytest.raises(ValueError):
        usr.add_user('a new user', {'foo': 'bar'})

def test_add_follower():
    usr.add_follower(usr.Investor, usr.Investor3)
    assert usr.follower_exists(usr.Investor,usr.Investor3)
    

def test_add_user():
    TEST_USER_NAME = 'testName'
    details = {}
    for field in usr.REQUIRED_FIELDS:
        if field==usr.FOLLOWERS or field==usr.FOLLOWING:
            details[field]=[]
        details[field] = 2
    usr.add_user(TEST_USER_NAME, details)
    assert usr.user_exists(TEST_USER_NAME)
    usr.del_user(TEST_USER_NAME)