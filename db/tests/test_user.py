import pytest

import db.user_types as usr
import db.coins as cn
# from server.tests.test_endpoints import TEST_CLIENT


def test_get_users():
    usrs = usr.get_users()
    assert isinstance(usrs, list)
    assert len(usrs) > 1


def test_get_users_dict():
    usrs = usr.get_users_dict()
    assert isinstance(usrs, dict)


def test_get_user_details():
    usr_dets = usr.get_user_type_details(usr.Investor)
    assert isinstance(usr_dets, dict)


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
    assert usr.follower_exists(usr.Investor, usr.Investor3)


def test_add_user():
    TEST_USER_NAME = 'testName'
    details = {}

    for field in usr.REQUIRED_FIELDS:
        details[field] = []
    usr.add_user(TEST_USER_NAME, details)
    assert usr.user_exists(TEST_USER_NAME)
    usr.del_user(TEST_USER_NAME)


def test_del_user():
    # adding temp user
    TEST_USER_NAME = 'testName'
    details = {}

    for field in usr.REQUIRED_FIELDS:
        details[field] = []
    usr.add_user(TEST_USER_NAME, details)
    # deleting user
    usr.del_user(TEST_USER_NAME)
    # if user not found -> PASS
    assert not usr.user_exists(TEST_USER_NAME)


def test_update_email():
    TEST_USER_NAME = 'testName'
    TEST_NEW_EMAIL = 'NEWSAMPLE@test.com'
    details = {}

    for field in usr.REQUIRED_FIELDS:
        details[field] = []
    usr.add_user(TEST_USER_NAME, details)
    usr.update_email(TEST_USER_NAME, TEST_NEW_EMAIL)
    assert usr.get_user_email(TEST_USER_NAME) == TEST_NEW_EMAIL
    usr.del_user(TEST_USER_NAME)


def test_get_user():
    TEST_USER_NAME = 'testName'
    details = {}

    for field in usr.REQUIRED_FIELDS:
        details[field] = []
    usr.add_user(TEST_USER_NAME, details)
    assert usr.get_user(TEST_USER_NAME) is not None
    usr.del_user(TEST_USER_NAME)


def test_get_password():
    credentials = usr.get_password(usr.Investor)
    assert isinstance(credentials, str)


def test_update_password():
    TEST_USER_NAME = 'testName'
    TEST_NEW_PASSWORD = 'abc123'
    details = {}
    for field in usr.REQUIRED_FIELDS:
        details[field] = []

    usr.add_user(TEST_USER_NAME, details)
    usr.update_password(TEST_USER_NAME, TEST_NEW_PASSWORD)
    assert usr.get_password(TEST_USER_NAME) == TEST_NEW_PASSWORD
    usr.del_user(TEST_USER_NAME)


def test_add_coin():
    usr.add_coin(usr.Investor, cn.coin_type['Bitcoin'])
    assert usr.user_coin_exists(usr.Investor, cn.coin_type['Bitcoin'])


def test_remove_coin():
    pass
