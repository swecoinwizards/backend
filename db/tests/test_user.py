import pytest
import os

import db.user_types as usr
import db.coins as cn
# import db.db_connect as dbc
# from server.tests.test_endpoints import TEST_CLIENT

RUNNING_ON_CICD_SERVER = os.environ.get('CI', False)
NEW_USER_DET = {'name': usr.TEST_USER_NAME, 'password': '****',
                'email': 'sampleuser@gmail.com'}
NEW_USER_DET2 = {'name': usr.TEST_USER_NAME2, 'password': '****',
                 'email': 'sampleuser@gmail.com'}


@pytest.fixture(scope='function')
def temp_user():
    usr.add_user(usr.TEST_USER_NAME, NEW_USER_DET)
    yield
    if (usr.user_exists(usr.TEST_USER_NAME)):
        usr.del_user(usr.TEST_USER_NAME)


@pytest.fixture(scope='function')
def temp_user2():
    usr.add_user(usr.TEST_USER_NAME2, NEW_USER_DET2)
    yield
    usr.del_user(usr.TEST_USER_NAME2)


def test_get_users(temp_user):
    usrs = usr.get_users()
    assert isinstance(usrs, list)


def test_get_posts(temp_user):
    posts = usr.get_posts(usr.TEST_USER_NAME)
    assert isinstance(posts, list)


# can remove this bc already have db one
def test_get_users_dict(temp_user):
    usrs = usr.get_users_dict()
    assert isinstance(usrs, dict)
    assert len(usrs) >= 1


def test_add_wrong_name_type():
    with pytest.raises(TypeError):
        usr.add_user(7, {})


def test_add_wrong_details_type():
    with pytest.raises(TypeError):
        usr.add_user('a new user', [])


def test_add_user_wrong_email():
    with pytest.raises(ValueError):
        usr.add_user('a new user', {
            'name': 'a new user',
            'password': '123',
            'email': 'invalidemail',
        })


def test_add_missing_field():
    with pytest.raises(ValueError):
        usr.add_user('a new user', {'foo': 'bar'})


def test_add_follower(temp_user, temp_user2):
    usr.add_follower(usr.TEST_USER_NAME, usr.TEST_USER_NAME2)
    assert usr.follower_exists(usr.TEST_USER_NAME, usr.TEST_USER_NAME2)


def test_remove_follower(temp_user, temp_user2):
    # usr.add_follower(usr.TEST_USER_NAME, usr.TEST_USER_NAME2)
    usr.add_follower(usr.TEST_USER_NAME, usr.TEST_USER_NAME2)
    usr.remove_follower(usr.TEST_USER_NAME, usr.TEST_USER_NAME2)
    assert not usr.follower_exists(usr.TEST_USER_NAME, usr.TEST_USER_NAME2)


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


def test_user_email(temp_user):
    assert isinstance(usr.get_user_email(usr.TEST_USER_NAME), str)


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


def test_change_username(temp_user):
    if not RUNNING_ON_CICD_SERVER:
        # TEST_USER_NAME = 'testName'
        NEW_USERNAME = 'abc123'
        usr.change_username(usr.TEST_USER_NAME, NEW_USERNAME)
        assert usr.user_exists(NEW_USERNAME)
        usr.del_user(NEW_USERNAME)


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
        usr.update_password(usr.TEST_USER_NAME, TEST_NEW_PASSWORD)
        assert usr.get_password(usr.TEST_USER_NAME) == TEST_NEW_PASSWORD


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


def test_profile_add_post(temp_user):
    TEST_POST = "Buy Bitcoin"
    usr.profile_add_post(usr.TEST_USER_NAME, TEST_POST)
    assert usr.access_profile_posts(usr.TEST_USER_NAME, 1) == TEST_POST


# @pytest.mark.skip(reason="Require add post to work")
def test_profile_remove_post(temp_user):
    # TEST_USER_NAME = 'testName'
    TEST_POST = "Buy Bitcoin NOW!"
    usr.profile_add_post(usr.TEST_USER_NAME, TEST_POST)
    assert usr.profile_delete_post(usr.TEST_USER_NAME, 0)


@pytest.mark.skip(reason="Require change post to work")
def test_modify_posts(temp_user):
    # should include post number
    post_number = 0
    assert usr.user_profile_change_post(usr.TEST_USER_NAME, post_number)


def test_user_login(temp_user):
    passw = usr.get_password(usr.TEST_USER_NAME)
    assert usr.user_login(usr.TEST_USER_NAME, passw)


def test_get_user_password(temp_user):
    passw = usr.get_password(usr.TEST_USER_NAME)
    assert isinstance(passw, str)
    assert passw is not None
    # assert passw == '****' or passw == 'abc123'


def test_user_login_fail(temp_user):
    with pytest.raises(Exception) as e:
        usr.user_login(usr.TEST_USER_NAME, 'WRONGPASSWORD')
    assert str(e.value) == "Wrong Password"


def test_get_coins(temp_user):
    assert isinstance(usr.get_coins(usr.TEST_USER_NAME), list)


def test_get_followers(temp_user):
    assert isinstance(usr.get_followers(usr.TEST_USER_NAME), list)


def test_get_followings(temp_user):
    assert isinstance(usr.get_followings(usr.TEST_USER_NAME), list)
