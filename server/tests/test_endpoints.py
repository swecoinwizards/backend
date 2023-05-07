import pytest
from unittest.mock import patch
import server.endpoints as ep
import db.user_types as user
import db.coins as cn

from http import HTTPStatus

TEST_CLIENT = ep.app.test_client()

TEST_COIN = 'TEST_COIN'
TEST_COIN_TICKER = 'TCN'
TEST_COIN_DETS = {'id': 3, 'name': TEST_COIN, 'symbol': TEST_COIN_TICKER,
                  'price': 1000}

SAMPLE_USER_NM = 'SampleUser'
SAMPLE_USER = {
    user.NAME: SAMPLE_USER_NM,
    user.PASSWORD: '***',
    user.EMAIL: '1@gmail.com',
    user.FOLLOWERS: [],
    user.FOLLOWING: [],
    user.COINS: [],
    user.POSTS: [],
}

NEW_USER_NM = 'NewUser'
NEW_USER = {
    user.NAME: NEW_USER_NM,
    user.PASSWORD: '***',
    user.EMAIL: '1@gmail.com',
}

BAD_USER_NM = 'BadNewUser'
BAD_USER = {
    user.NAME: BAD_USER_NM,
    user.PASSWORD: '',
}

SAMPLE_USER_NM2 = 'SampleUserToo'
SAMPLE_USER2 = {
    user.NAME: SAMPLE_USER_NM2,
    user.PASSWORD: '***',
    user.EMAIL: '1@gmail.com',
    user.FOLLOWERS: [],
    user.FOLLOWING: [],
    user.COINS: [],
    user.POSTS: [],
}


@pytest.fixture(scope='function')
def temp_user():
    user.add_user(SAMPLE_USER_NM, SAMPLE_USER)
    user.add_user(SAMPLE_USER_NM2, SAMPLE_USER2)
    yield
    user.del_user(SAMPLE_USER_NM)
    user.del_user(SAMPLE_USER_NM2)


@pytest.fixture(scope='function')
def temp_coin():
    cn.save_coin(TEST_COIN, TEST_COIN_DETS)
    yield
    cn.remove_coin(TEST_COIN)


@pytest.fixture(scope='function')
def temp_coin_user():
    user.add_user(SAMPLE_USER_NM, SAMPLE_USER)
    cn.save_coin(TEST_COIN, TEST_COIN_DETS)
    yield
    user.del_user(SAMPLE_USER_NM)
    cn.remove_coin(TEST_COIN)


def test_hello():
    """
    See if Hello works.
    """
    resp_json = TEST_CLIENT.get(ep.API_PFX + ep.HELLO).get_json()
    assert isinstance(resp_json[ep.MESSAGE], str)


def test_get_user_list():
    """
    See if we can get a user list properly.
    Return should look like:
        {USER_LIST_NM: [list of users types...]}
    """
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_LIST}').get_json()
    assert isinstance(resp_json, dict)
    assert isinstance(resp_json[ep.USER_LIST_NM], list)


def test_get_user_names_list():
    """
    Check returns user name list
    """
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_LIST}/{ep.NAMES}').get_json()
    assert isinstance(resp_json, list)


def test_add_user():
    """
    Test adding a user.
    """
    resp = TEST_CLIENT.post(f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_ADD}', json=NEW_USER)
    assert user.user_exists(NEW_USER_NM)
    assert resp.status_code == HTTPStatus.OK
    user.del_user(NEW_USER_NM)


def test_add_user_fail():
    """
    Test adding a user.
    """
    with pytest.raises(Exception):
        resp = TEST_CLIENT.post(f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_ADD}', json=BAD_USER)
        assert user.user_exists(BAD_USER_NM)
        user.del_user(NEW_USER_NM)


# @pytest.mark.skip(reason="Will come back after adding remove func w/pymongo")
@patch('db.user_types.del_user', return_value=True)
def test_remove_user(mock_user_details):
    """
    Test removing a user.
    """
    # user.del_user(SAMPLE_USER_NM)
    resp = TEST_CLIENT.delete(f'{ep.API_PFX}/{ep.USERS_NS}{ep.REMOVE_USER}'
                                + f'/{SAMPLE_USER_NM}')
    assert not user.user_exists(SAMPLE_USER_NM)


def test_remove_user_fail():
    """
    Test removing a user.
    """
    resp = TEST_CLIENT.delete(f'{ep.API_PFX}/{ep.USERS_NS}{ep.REMOVE_USER}/10x')
    assert resp.status_code==HTTPStatus.NOT_FOUND


@patch('db.user_types.get_user', return_value=SAMPLE_USER)
def test_get_user_type_details(mock_user_details):
    """
    Testing getting user data using patch
    """
    resp = TEST_CLIENT.get(f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_DETAILS}'
                                + f'/{SAMPLE_USER_NM}')
    resp_json = resp.get_json()
    assert SAMPLE_USER_NM in resp_json['Data']
    assert isinstance(resp_json['Data'][SAMPLE_USER_NM], dict)
    assert resp.status_code == HTTPStatus.OK


def test_get_user_type_details_null():
    """
    Testing getting user data using patch
    """
    resp_json = TEST_CLIENT.get(f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_DETAILS}'
                                + f'/NotAUser')
    assert resp_json.status_code == HTTPStatus.NOT_FOUND


def test_add_follower(temp_user):
    resp_json = TEST_CLIENT.post(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_FOLLOW}/{SAMPLE_USER_NM}/'
        + f'{SAMPLE_USER_NM2}').get_json()
    print(resp_json, f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_FOLLOW}/{SAMPLE_USER_NM}/{SAMPLE_USER_NM2}')
    assert isinstance(resp_json, dict)


@patch('db.user_types.add_following', side_effect=ValueError())
def test_add_follower_fail(mock_user_details):
    resp = TEST_CLIENT.post(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_FOLLOW}/{SAMPLE_USER_NM}/{SAMPLE_USER_NM2}')
    resp_json = resp.get_json()
    print(resp_json, f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_FOLLOW}/{SAMPLE_USER_NM}/{SAMPLE_USER_NM2}')
    assert isinstance(resp_json, dict)
    assert resp.status_code == HTTPStatus.BAD_REQUEST


def test_remove_follower(temp_user):
    follow_resp = TEST_CLIENT.post(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_FOLLOW}/{SAMPLE_USER_NM}/{SAMPLE_USER_NM2}')

    resp_json = TEST_CLIENT.delete(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_REMOVE_FOLLOW}/{SAMPLE_USER_NM}' +
        f'/{SAMPLE_USER_NM2}').get_json()
    assert isinstance(resp_json, dict)


def test_remove_follower_fail(temp_user):
    resp = resp_json = TEST_CLIENT.delete(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_REMOVE_FOLLOW}/{SAMPLE_USER_NM}' +
        f'/{SAMPLE_USER_NM2}')
    resp_json = resp.get_json()
    print(resp_json)
    assert isinstance(resp_json, dict)
    assert resp.status_code == HTTPStatus.BAD_REQUEST


def test_user_followers(temp_user):
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_FOLLOWERS}/{SAMPLE_USER_NM}'
        ).get_json()
    assert isinstance(resp_json, dict)


def test_user_followers_fail():
    resp = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_FOLLOWERS}/badUSER'
        )
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert "Error" in resp_json['Data']


def test_user_followings(temp_user):
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_FOLLOWINGS}/{SAMPLE_USER_NM}'
        ).get_json()
    assert isinstance(resp_json, dict)


def test_user_followings_fail():
    resp = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_FOLLOWINGS}/badUSER'
        )
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert "Error" in resp_json['Data']


def test_user_login(temp_user):
    password = '***'
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_LOGIN}'
        + f'/{SAMPLE_USER_NM}/{password}'
        ).get_json()
    assert isinstance(resp_json, dict)


def test_user_login_fail(temp_user):
    password = "WRONGPASSWORD"
    resp = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_LOGIN}'
        + f'/{SAMPLE_USER_NM}/{password}'
        )
    assert resp.status_code == HTTPStatus.UNAUTHORIZED


def test_user_update_password(temp_user):
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_UPDATE}', json={}
        ).get_json()
    assert isinstance(resp_json, dict)


@patch('db.coins.coin_details', return_value={})
def test_coin_type_details(mock_coin_details):
    """
    """
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.COINS_NS}{ep.COIN_DETAILS}/'
        + f'{TEST_COIN}').get_json()
    assert isinstance(resp_json, dict)


def test_coin_tickers_list():
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.COINS_NS}{ep.COIN_TICKERS_LIST}').get_json()
    assert isinstance(resp_json, dict)


def test_coin_type_details_fail():
    """
    """
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.COINS_NS}{ep.COIN_DETAILS}/'
        + f'{TEST_COIN}').get_json()
    print(resp_json)
    assert isinstance(resp_json["message"], str)


@patch('db.coins.new_coin_details', return_value={})
def test_get_new_coin(mock_coin_details):
    resp = TEST_CLIENT.put(
        f'{ep.API_PFX}/{ep.COINS_NS}{ep.COIN_ADD}/'
        + f'{TEST_COIN}')
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert resp.status_code == HTTPStatus.OK


@patch('db.coins.new_coin_details', side_effect=Exception())
def test_get_new_coin_fail(mock_coin_details):
    resp = TEST_CLIENT.put(
        f'{ep.API_PFX}/{ep.COINS_NS}{ep.COIN_ADD}/'
        + f'{TEST_COIN}')
    resp_json = resp.get_json()
    print(resp_json)
    assert isinstance(resp_json["message"], str)
    assert "Error" in resp_json["message"]


def test_get_coin_list():
    """
    See if we can get a user list properly.
    Return should look like:
        {USER_LIST_NM: [list of users types...]}
    """
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.COINS_NS}{ep.COIN_LIST}'
        ).get_json()
    assert isinstance(resp_json[ep.COIN_LIST_NM], list)


def test_add_coin(temp_coin_user):
    resp_json = TEST_CLIENT.put(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.COIN_FOLLOW}/{SAMPLE_USER_NM}' +
        f'/{TEST_COIN}'
        ).get_json()
    assert isinstance(resp_json, dict)


def test_add_coin_fail():
    resp_json = TEST_CLIENT.put(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.COIN_FOLLOW}/{SAMPLE_USER_NM}' +
        f'/{TEST_COIN}'
        ).get_json()
    assert isinstance(resp_json['message'], str)
    assert "Error" in resp_json['message']


def test_remove_coin(temp_coin_user):
    resp_json = TEST_CLIENT.put(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.COIN_REMOVE_FOLLOW}/' +
        f'{SAMPLE_USER_NM}/{TEST_COIN}'
        ).get_json()
    assert isinstance(resp_json, dict)


def test_remove_coin_fail():
    resp_json = TEST_CLIENT.put(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.COIN_REMOVE_FOLLOW}/' +
        f'{SAMPLE_USER_NM}/{TEST_COIN}'
        ).get_json()
    assert isinstance(resp_json['message'], str)
    assert "Error" in resp_json['message']



@patch('db.coins.coin_exists', return_value=True)
def test_coin_exists(mock_coin_details):
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.COINS_NS}/{ep.EXIST}/{TEST_COIN}'
        ).get_json()
    assert isinstance(resp_json, bool)
    assert resp_json==True


def test_coin_exists_false():
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.COINS_NS}/{ep.EXIST}/{TEST_COIN}'
        ).get_json()
    assert isinstance(resp_json, bool)
    assert resp_json==False  


def test_get_coin_dict():
    resp_json = TEST_CLIENT.get(f'{ep.API_PFX}/{ep.COINS_NS}{ep.COIN_DICT}'
                                ).get_json()
    assert isinstance(resp_json, dict)


@patch('db.user_types.user_coin_exists', return_value=True)
def test_coin_exists_in_user(mock_user_details):
    print(f'{ep.API_PFX}/{ep.USERS_NS}{ep.COIN_EXISTS}/{SAMPLE_USER_NM}/{TEST_COIN}')
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.COIN_EXISTS}/{SAMPLE_USER_NM}/{TEST_COIN}'
        ).get_json()
    assert isinstance(resp_json, bool)


@patch('db.user_types.user_coin_exists', return_value=False)
def test_coin_exists_in_user_false(mock_user_details):
    print(f'{ep.API_PFX}/{ep.USERS_NS}{ep.COIN_EXISTS}/{SAMPLE_USER_NM}/{TEST_COIN}')
    resp_json = TEST_CLIENT.get(
        f'{ep.API_PFX}/{ep.USERS_NS}{ep.COIN_EXISTS}/{SAMPLE_USER_NM}/{TEST_COIN}'
        ).get_json()
    assert isinstance(resp_json, bool)


def test_get_post_all():
    resp_json = TEST_CLIENT.get(f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_POSTS}/{ep.LIST}/'
                                ).get_json()
    assert isinstance(resp_json, dict)


def test_get_post_empty(temp_user):
    resp_json = TEST_CLIENT.get(f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_POSTS}/{ep.LIST}/badTerm'
                                ).get_json()
    print(resp_json)
    assert isinstance(resp_json, dict)
    assert len(resp_json["Data"]["posts"])==0


@patch('db.user_types.get_all_posts', return_value=["post1"])
def test_get_post_success(mock_user_details):
    resp_json = TEST_CLIENT.get(f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_POSTS}/{ep.LIST}/term'
                                ).get_json()
    assert isinstance(resp_json, dict)
    assert len(resp_json["Data"]["posts"])>0


@patch('db.user_types.get_all_posts', side_effect=Exception())
def test_get_post_no_users(mock_user_details):
    resp = TEST_CLIENT.get(f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_POSTS}/{ep.LIST}/term')
    resp_json = resp.get_json()
    assert resp.status_code == HTTPStatus.NOT_FOUND


def test_get_user_posts(temp_user):
    resp = TEST_CLIENT.get(f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_POSTS}/{SAMPLE_USER_NM}')
    resp_json = resp.get_json()
    assert isinstance(resp_json,dict)


def test_get_user_posts_fail():
    resp = TEST_CLIENT.get(f'{ep.API_PFX}/{ep.USERS_NS}{ep.USER_POSTS}/BADUSER')
    resp_json = resp.get_json()
    assert isinstance(resp_json["message"],str)
    assert resp.status_code == HTTPStatus.NOT_FOUND


def test_main_menu():
    resp_json = TEST_CLIENT.get(ep.API_PFX + ep.MAIN_MENU).get_json()
    assert isinstance(resp_json,dict)


def test_options_menu():
    resp_json = TEST_CLIENT.get(ep.API_PFX + ep.OPTIONS).get_json()
    assert isinstance(resp_json,dict)


def test_endpoints_documentation():
    resp_json = TEST_CLIENT.get(f'{ep.API_PFX}/endpoints').get_json()
    assert isinstance(resp_json,dict)