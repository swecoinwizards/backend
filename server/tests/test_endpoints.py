# import pytest

import server.endpoints as ep
import db.user_types as user

TEST_CLIENT = ep.app.test_client()

TEST_USER_TYPE = 'Investor'

TEST_USER_TYPE2 = 'Investor2'

TEST_COIN_TYPE = 'Bitcoin'

SAMPLE_USER_NM = 'SampleUser'
SAMPLE_USER = {
    user.NAME: SAMPLE_USER_NM,
    user.PASSWORD: '***',
    user.EMAIL: '1@gmail.com',
    user.FOLLOWERS: [],
    user.FOLLOWING: [],
    user.COINS: [],
}


SAMPLE_USER_NM2 = 'SampleUser'
SAMPLE_USER2 = {
    user.NAME: SAMPLE_USER_NM2,
    user.PASSWORD: '***',
    user.EMAIL: '1@gmail.com',
    user.FOLLOWERS: [],
    user.FOLLOWING: [],
    user.COINS: [],
}


def test_hello():
    """
    See if Hello works.
    """
    resp_json = TEST_CLIENT.get(ep.HELLO).get_json()
    assert isinstance(resp_json[ep.MESSAGE], str)


def test_get_user_list():
    """
    See if we can get a user list properly.
    Return should look like:
        {USER_LIST_NM: [list of users types...]}
    """
    resp_json = TEST_CLIENT.get(ep.USER_LIST).get_json()
    assert isinstance(resp_json[ep.USER_LIST_NM], list)


def test_add_user():
    """
    Test adding a user.
    """
    # print("pls work ", SAMPLE_USER.keys())
    # resp = TEST_CLIENT.post(ep.USER_ADD, json=SAMPLE_USER)
    assert user.user_exists(SAMPLE_USER_NM)
    user.del_user(SAMPLE_USER_NM)


def test_remove_user():
    """
    Test adding a user.
    """
    # print("pls work ", SAMPLE_USER.keys())
    # resp = TEST_CLIENT.post(ep.USER_ADD, json=SAMPLE_USER)
    assert not user.user_exists(SAMPLE_USER_NM)


def test_get_user_type_details():
    """
    """
    resp_json = TEST_CLIENT.get(f'{ep.USER_DETAILS}/{TEST_USER_TYPE}'
                                ).get_json()
    assert TEST_USER_TYPE in resp_json
    assert isinstance(resp_json[TEST_USER_TYPE], dict)


def test_get_users_dict():
    resp_json = TEST_CLIENT.get(f'{ep.USER_DICT}'
                                ).get_json()
    assert isinstance(resp_json, dict)


def test_add_follower():
    user.add_user(SAMPLE_USER_NM, SAMPLE_USER)
    user.add_user(SAMPLE_USER_NM2, SAMPLE_USER2)
    resp_json = TEST_CLIENT.get(
        f'{ep.USER_FOLLOW}/{SAMPLE_USER}/{SAMPLE_USER2}').get_json()
    # print(resp_json)
    assert isinstance(resp_json, dict)


def test_remove_follower():
    resp_json = TEST_CLIENT.get(
        f'{ep.USER_REMOVE_FOLLOW}/{SAMPLE_USER}/{SAMPLE_USER2}').get_json()
    assert isinstance(resp_json, dict)


def test_user_followers():
    resp_json = TEST_CLIENT.get(
        f'{ep.USER_FOLLOWERS}/{SAMPLE_USER}').get_json()
    assert isinstance(resp_json, dict)


def test_user_login():
    password = '***'
    resp_json = TEST_CLIENT.get(
        f'{ep.USER_LOGIN}/{SAMPLE_USER_NM}/{password}').get_json()
    assert isinstance(resp_json, dict)


def test_user_login_fail():
    # with pytest.raises(Exception) as e:
    password = "WRONGPASSWORD"
    resp_json = TEST_CLIENT.get(
        f'{ep.USER_LOGIN}/{SAMPLE_USER_NM}/{password}').get_json()
    assert resp_json['Data'] == "Cannot login: Wrong Password"


def test_coin_type_details():
    """
    """
    resp_json = TEST_CLIENT.get(f'{ep.COIN_DETAILS}/{TEST_COIN_TYPE}'
                                ).get_json()
    assert TEST_COIN_TYPE in resp_json
    assert isinstance(resp_json[TEST_COIN_TYPE], dict)


def test_get_coin_list():
    """
    See if we can get a user list properly.
    Return should look like:
        {USER_LIST_NM: [list of users types...]}
    """
    resp_json = TEST_CLIENT.get(ep.COIN_LIST).get_json()
    assert isinstance(resp_json[ep.COIN_LIST_NM], list)


def test_add_coin():
    user.add_user(SAMPLE_USER_NM, SAMPLE_USER)
    resp_json = TEST_CLIENT.get(
        f'{ep.COIN_FOLLOW}/{SAMPLE_USER}/{TEST_COIN_TYPE}').get_json()
    # print(resp_json)
    assert isinstance(resp_json, dict)


def test_remove_coin():
    resp_json = TEST_CLIENT.get(
        f'{ep.COIN_REMOVE_FOLLOW}/{SAMPLE_USER}/{TEST_COIN_TYPE}').get_json()
    assert isinstance(resp_json, dict)
