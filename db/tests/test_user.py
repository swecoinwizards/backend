import pytest
import os

import db.user_types as usr
import db.coins as cn
# import db.db_connect as dbc
# from server.tests.test_endpoints import TEST_CLIENT

RUNNING_ON_CICD_SERVER = os.environ.get('CI', False)
NEW_USER_DET = {'name': usr.TEST_USER_NAME, 'password': '****',
                'email': 'sampleuser@gmail.com', 'Followers': [],
                'Following': [], 'coins': [], 'posts': []}


@pytest.fixture(scope='function')
def temp_user():
    usr.add_user(usr.TEST_USER_NAME, NEW_USER_DET)
    yield
    usr.del_user(usr.TEST_USER_NAME)


def test_get_users_db(temp_user):
    if not RUNNING_ON_CICD_SERVER:
        usrs = usr.get_users_db()
        assert isinstance(usrs, list)
        assert len(usrs) > 1


def test_get_users_dict_db(temp_user):
    if not RUNNING_ON_CICD_SERVER:
        usrs = usr.get_users_dict_db()
        assert isinstance(usrs, dict)
        assert len(usrs) > 1


def test_get_users(temp_user):
    usrs = usr.get_users()
    assert isinstance(usrs, list)
    assert len(usrs) > 1


def test_get_posts(temp_user):
    posts = usr.get_posts(usr.TEST_USER_NAME)
    assert isinstance(posts, list)


# can remove this bc already have db one
def test_get_users_dict(temp_user):
    usrs = usr.get_users_dict()
    assert isinstance(usrs, dict)


def test_get_user_details(temp_user):
    usr_dets = usr.get_user_type_details(usr.TEST_USER_NAME)
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


def test_add_follower(temp_user):
    usr.add_follower(usr.TEST_USER_NAME, usr.Investor3)
    assert usr.follower_exists(usr.TEST_USER_NAME, usr.Investor3)


def test_add_user(temp_user):
    if not RUNNING_ON_CICD_SERVER:
        # TEST_USER_NAME = 'testName'
        # details = {'name': TEST_USER_NAME}

        # for field in usr.REQUIRED_FIELDS[1:]:
        #     details[field] = []
        # usr.add_user(TEST_USER_NAME, details)
        assert usr.user_exists(usr.TEST_USER_NAME)
        # usr.del_user(TEST_USER_NAME)


def test_del_user(temp_user):
    if not RUNNING_ON_CICD_SERVER:
        # deleting user
        usr.del_user(usr.TEST_USER_NAME)
        # if user not found -> PASS
        assert usr.user_exists(usr.TEST_USER_NAME) is False
        usr.add_user(usr.TEST_USER_NAME, NEW_USER_DET)


def test_update_email(temp_user):
    if not RUNNING_ON_CICD_SERVER:
        # TEST_USER_NAME = 'testName'
        TEST_NEW_EMAIL = 'NEWSAMPLE@test.com'
        # details = {'name': TEST_USER_NAME}

        # for field in usr.REQUIRED_FIELDS[1:]:
        #     details[field] = []
        # usr.add_user(TEST_USER_NAME, details)
        usr.update_email(usr.TEST_USER_NAME, TEST_NEW_EMAIL)
        assert usr.get_user_email(usr.TEST_USER_NAME) == TEST_NEW_EMAIL
        # usr.del_user(usr.TEST_USER_NAME)


def test_get_user(temp_user):
    if not RUNNING_ON_CICD_SERVER:
        # TEST_USER_NAME = 'testName'
        # details = {'name': TEST_USER_NAME}

        # for field in usr.REQUIRED_FIELDS[1:]:
        #     details[field] = []
        # usr.add_user(TEST_USER_NAME, details)
        assert usr.get_user(usr.TEST_USER_NAME) is not None
        # usr.del_user(usr.TEST_USER_NAME)


def test_get_password(temp_user):
    credentials = usr.get_password(usr.TEST_USER_NAME)
    assert isinstance(credentials, str)


def test_update_password(temp_user):
    if not RUNNING_ON_CICD_SERVER:
        # TEST_USER_NAME = 'testName'
        TEST_NEW_PASSWORD = 'abc123'
        # details = {'name': TEST_USER_NAME}
        # for field in usr.REQUIRED_FIELDS[1:]:
        #     details[field] = []

        # usr.add_user(TEST_USER_NAME, details)
        usr.update_password(usr.TEST_USER_NAME, TEST_NEW_PASSWORD)
        assert usr.get_password(usr.TEST_USER_NAME) == TEST_NEW_PASSWORD
        # usr.del_user(usr.TEST_USER_NAME)


def test_add_coin(temp_user):
    # Might need to change how coins are stored into the user,
    # currently storing an instance of 'Bitcoin' dict
    # which will be hard to keep track of as its attributes like price
    # change, (e.g. can't remove if price updates from API call as
    # everything stored will be outdated)
    usr.add_coin(usr.TEST_USER_NAME, cn.coin_type['Bitcoin'])
    assert usr.user_coin_exists(usr.TEST_USER_NAME, cn.coin_type['Bitcoin'])
    usr.remove_coin(usr.TEST_USER_NAME, cn.coin_type['Bitcoin'])


def test_user_coin_evaluation(temp_user):
    usr.add_coin(usr.TEST_USER_NAME, cn.coin_type['Bitcoin'])
    assert usr.user_coin_valuation(usr.TEST_USER_NAME) >= 0
    usr.remove_coin(usr.TEST_USER_NAME, cn.coin_type['Bitcoin'])


@pytest.mark.skip(reason="Will come back to it after")
def test_profile_add_post():
    TEST_USER_NAME = 'testName'
    TEST_POST = "Buy Bitcoin NOW!"
    details = {'name': TEST_USER_NAME}
    for field in usr.REQUIRED_FIELDS[1:]:
        details[field] = []
    usr.add_user(TEST_USER_NAME, details)
    usr.user_profile_add_post(TEST_USER_NAME, TEST_POST)
    assert len(usr.get_posts(TEST_USER_NAME)) > 0
    usr.del_user(TEST_USER_NAME)


@pytest.mark.skip(reason="Require add post to work")
def test_profile_remove_post():
    TEST_USER_NAME = 'testName'
    TEST_POST = "Buy Bitcoin NOW!"
    details = {'name': TEST_USER_NAME}
    for field in usr.REQUIRED_FIELDS[1:]:
        details[field] = []
    usr.add_user(TEST_USER_NAME, details)
    usr.user_profile_add_post(TEST_USER_NAME, TEST_POST)
    assert usr.user_profile_delete_post(TEST_USER_NAME, 0)


# def test_remove_coin():
#     pass


def test_user_login(temp_user):
    assert usr.user_login(usr.TEST_USER_NAME, '****')


def test_get_user_password(temp_user):
    assert isinstance(usr.get_password(usr.TEST_USER_NAME), str)


def test_user_login_fail(temp_user):
    with pytest.raises(Exception) as e:
        usr.user_login(usr.TEST_USER_NAME, 'WRONGPASSWORD')
    assert str(e.value) == "Wrong Password"


def test_get_followers(temp_user):
    assert isinstance(usr.get_followers(usr.TEST_USER_NAME), list)
