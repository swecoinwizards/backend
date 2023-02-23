import pytest

import server.endpoints as ep
import db.user_types as user

TEST_CLIENT = ep.app.test_client()

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


SAMPLE_USER_NM2 = 'SampleUserToo'
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
    resp_json = TEST_CLIENT.get(f'{ep.USERS_NS}{ep.USER_LIST}').get_json()
    print(resp_json, f'users/{ep.USER_LIST}')
    assert isinstance(resp_json[ep.USER_LIST_NM], list)


def test_add_user():
    """
    Test adding a user.
    """
    user.add_user(SAMPLE_USER_NM, SAMPLE_USER)
    assert user.user_exists(SAMPLE_USER_NM)
    user.del_user(SAMPLE_USER_NM)


@pytest.mark.skip(reason="Will come back after adding remove func w/pymongo")
def test_remove_user():
    """
    Test adding a user.
    """
    user.del_user(SAMPLE_USER_NM)
    assert not user.user_exists(SAMPLE_USER_NM)


@pytest.fixture(scope='function')
def temp_user():
    user.add_user(SAMPLE_USER_NM, SAMPLE_USER)
    yield
    user.del_user(SAMPLE_USER_NM)


def test_get_user_type_details(temp_user):
    """
    """
    resp_json = TEST_CLIENT.get(f'{ep.USERS_NS}{ep.USER_DETAILS}' +
                                f'/{SAMPLE_USER_NM}').get_json()
    assert SAMPLE_USER_NM in resp_json['Data']
    assert isinstance(resp_json['Data'][SAMPLE_USER_NM], dict)


def test_get_users_dict():
    resp_json = TEST_CLIENT.get(f'{ep.USERS_NS}{ep.USER_DICT}'
                                ).get_json()
    assert isinstance(resp_json, dict)


def test_add_follower():
    resp_json = TEST_CLIENT.get(
        f'{ep.USERS_NS}{ep.USER_FOLLOW}/{SAMPLE_USER}/'
        + f'{SAMPLE_USER2}').get_json()
    assert isinstance(resp_json, dict)


def test_remove_follower():
    resp_json = TEST_CLIENT.get(
        f'{ep.USERS_NS}{ep.USER_REMOVE_FOLLOW}/{SAMPLE_USER}' +
        f'/{SAMPLE_USER2}').get_json()
    assert isinstance(resp_json, dict)


def test_user_followers():
    resp_json = TEST_CLIENT.get(
        f'{ep.USERS_NS}{ep.USER_FOLLOWERS}/{SAMPLE_USER}').get_json()
    assert isinstance(resp_json, dict)


def test_user_login(temp_user):
    password = '***'
    resp_json = TEST_CLIENT.get(
        f'{ep.USERS_NS}{ep.USER_LOGIN}/{SAMPLE_USER_NM}/{password}').get_json()
    assert isinstance(resp_json, dict)


def test_user_login_fail(temp_user):
    password = "WRONGPASSWORD"
    resp_json = TEST_CLIENT.get(
        f'{ep.USERS_NS}{ep.USER_LOGIN}/{SAMPLE_USER_NM}/{password}').get_json()
    assert resp_json['Data'] == "Cannot login: Wrong Password"


def test_user_update_password():
    resp_json = TEST_CLIENT.get(
        f'{ep.USERS_NS}{ep.USER_UPDATE_PASSWORD}', json={}).get_json()
    print(resp_json)
    assert isinstance(resp_json, dict)


@pytest.mark.skip(reason="Coindb empty at start; causes test to fail")
def test_coin_type_details():
    """
    """
    resp_json = TEST_CLIENT.get(f'{ep.COINS_NS}{ep.COIN_DETAILS}/' +
                                f'{TEST_COIN_TYPE}').get_json()
    assert TEST_COIN_TYPE in resp_json
    assert isinstance(resp_json[TEST_COIN_TYPE], dict)


def test_get_coin_list():
    """
    See if we can get a user list properly.
    Return should look like:
        {USER_LIST_NM: [list of users types...]}
    """
    resp_json = TEST_CLIENT.get(f'{ep.COINS_NS}{ep.COIN_LIST}').get_json()
    assert isinstance(resp_json[ep.COIN_LIST_NM], list)


def test_add_coin():
    resp_json = TEST_CLIENT.get(
        f'{ep.USERS_NS}{ep.COIN_FOLLOW}/{SAMPLE_USER}' +
        f'/{TEST_COIN_TYPE}').get_json()
    assert isinstance(resp_json, dict)


def test_remove_coin():
    resp_json = TEST_CLIENT.get(
        f'{ep.USERS_NS}{ep.COIN_REMOVE_FOLLOW}/' +
        f'{SAMPLE_USER}/{TEST_COIN_TYPE}').get_json()
    assert isinstance(resp_json, dict)


def test_get_coin_dict():
    resp_json = TEST_CLIENT.get(f'{ep.COINS_NS}{ep.COIN_DICT}'
                                ).get_json()
    assert isinstance(resp_json, dict)
