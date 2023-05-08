import pytest
import os

import db.user_types as usr
import db.coins as cn
from unittest.mock import patch
# import db.db_connect as dbc
# from server.tests.test_endpoints import TEST_CLIENT

RUNNING_ON_CICD_SERVER = os.environ.get('CI', False)

TEST_USER_NAME = "RANDOMUSER"
TEST_USER_NAME2 = "RANDOMUSER2"
TEST_USER_NAME3 = "RANDOMUSER3"

NEW_USER_DET = {'name': TEST_USER_NAME, 'password': '****',
                'email': 'sampleuser@gmail.com'}
NEW_USER_DET2 = {'name': TEST_USER_NAME2, 'password': '****',
                 'email': 'sampleuser@gmail.com'}
NEW_USER_DET3 = {'name': TEST_USER_NAME3, 'password': '****',
                 'email': 'sampleuser33@gmail.com'}



@pytest.fixture(scope='function')
def temp_user():
    usr.add_user(TEST_USER_NAME, NEW_USER_DET)
    yield
    if (usr.user_exists(TEST_USER_NAME)):
        usr.del_user(TEST_USER_NAME)


@pytest.fixture(scope='function')
def temp_user2():
    usr.add_user(TEST_USER_NAME2, NEW_USER_DET2)
    yield
    usr.del_user(TEST_USER_NAME2)


@pytest.fixture(scope='function')
def temp_user3():
    usr.add_user(TEST_USER_NAME3, NEW_USER_DET3)
    yield
    usr.del_user(TEST_USER_NAME3)


TEST_COIN = 'TEST_COIN'
TEST_COIN_TICKER = 'TCN'
TEST_COIN_DETS = {'id': 3, 'name': TEST_COIN, 'symbol': TEST_COIN_TICKER,
                  'price': 1000}

TEST_TITLE = 'TITLE'
TEST_CONTENT = 'TEST'
TEST_TAGS = ['TEST']

RUNNING_ON_CICD_SERVER = os.environ.get('CI', False)


@pytest.fixture(scope='function')
def temp_user_coin():
    usr.add_user(TEST_USER_NAME, NEW_USER_DET)
    cn.save_coin(TEST_COIN, TEST_COIN_DETS)
    yield
    cn.remove_coin(TEST_COIN)
    if (usr.user_exists(TEST_USER_NAME)):
        usr.del_user(TEST_USER_NAME)


def test_get_users():
    usrs = usr.get_users()
    assert isinstance(usrs, list)


def test_get_user_names():
    usrs = usr.get_user_names()
    assert isinstance(usrs, list)


def test_get_posts(temp_user):
    posts = usr.get_posts(TEST_USER_NAME)
    assert isinstance(posts, list)


def test_get_posts_fail():
    with pytest.raises(ValueError):
        usr.get_posts("DoesNotExist")
        usr.get_posts("")
        usr.get_posts(" ")


def test_add_wrong_name_type():
    with pytest.raises(TypeError):
        usr.add_user(7, {'name': 7,
                         'password': '****', 'email':
                         'sampleuser@gmail.com'})
        usr.add_user(' ', {'name': 'name',
                           'password': '****', 'email':
                           'sampleuser@gmail.com'})


def test_add_wrong_details_type():
    with pytest.raises(TypeError):
        usr.add_user('a new user', [])
        usr.add_user('newU', {'name': 'newU',
                              'email':
                              'sampleuser@gmail.com'})
        usr.add_user('newU', {'name': 'newU',
                              'password': ' ', 'email':
                              'sampleuser@gmail.com'})
        usr.add_user('newU', {'name': 'newU',
                              'password': 1, 'email':
                              'sampleuser@gmail.com'})
        usr.add_user('newU', {'name': 'newU',
                              'password': ' ', 'email':
                              'sampleusergmail.com'})
        usr.add_user('newU', {'name': ' ',
                              'password': '**', 'email':
                              'sampleusergmail.com'})
        usr.add_user('newU', {'name': 'newU',
                              'password': '', 'email':
                              'sampleusergmail.com'})


def test_add_user_wrong_email():
    with pytest.raises(ValueError):
        usr.add_user('aNewUser', {
            'name': 'aNewUser',
            'password': '123',
            'email': 'invalidemail',
        })
        usr.add_user('aNewUser', {
                    'name': 'Newuser',
                    'password': '123',
                    'email': 'invalidemail@gmailcom'})


def test_add_missing_field():
    with pytest.raises(ValueError):
        usr.add_user('a new user', {'foo': 'bar'})


def test_add_following(temp_user, temp_user2):
    """
    temp_user will follow temp_user2
    """
    usr.add_following(TEST_USER_NAME, TEST_USER_NAME2)
    assert usr.following_exists(TEST_USER_NAME, TEST_USER_NAME2)


def test_add_following_fail():
    with pytest.raises(ValueError):
        usr.add_following(TEST_USER_NAME, 'fakeName')


def test_remove_follow(temp_user, temp_user2):
    usr.add_following(TEST_USER_NAME, TEST_USER_NAME2)
    usr.remove_follow(TEST_USER_NAME, TEST_USER_NAME2)
    assert not usr.following_exists(TEST_USER_NAME, TEST_USER_NAME2)
    assert not usr.follower_exists(TEST_USER_NAME2, TEST_USER_NAME)


def test_remove_following_fail():
    with pytest.raises(ValueError):
        usr.remove_follow(TEST_USER_NAME, "fakeName")


def test_add_user(temp_user):
    assert usr.user_exists(TEST_USER_NAME)


def test_add_user_fail(temp_user):
    with pytest.raises(ValueError):
        usr.add_user(TEST_USER_NAME, NEW_USER_DET)


def test_del_user(temp_user):
    # deleting user
    usr.del_user(TEST_USER_NAME)
    # if user not found -> PASS
    assert usr.user_exists(TEST_USER_NAME) is False
    usr.add_user(TEST_USER_NAME, NEW_USER_DET)


def test_del_user_fail(temp_user):
    with pytest.raises(ValueError):
        usr.del_user("fakeUser")


def test_user_email(temp_user):
    assert isinstance(usr.get_user_email(TEST_USER_NAME), str)


def test_user_email_fail(temp_user):
    with pytest.raises(ValueError):
        usr.get_user_email("fakeUser")


def test_update_email(temp_user):
    TEST_NEW_EMAIL = 'NEWSAMPLE@test.com'
    usr.update_fields(TEST_USER_NAME, "", TEST_NEW_EMAIL)
    assert usr.get_user_email(TEST_USER_NAME) == TEST_NEW_EMAIL


def test_update_email_fail(temp_user):
    TEST_NEW_EMAIL = 'NEWSAMPLEtest.com'
    with pytest.raises(ValueError):
        usr.update_fields(TEST_USER_NAME, "", TEST_NEW_EMAIL)
        assert usr.get_user_email(TEST_USER_NAME) == TEST_NEW_EMAIL


def test_update_email_fail_type(temp_user):
    TEST_NEW_EMAIL = 123
    with pytest.raises(TypeError):
        usr.update_fields(TEST_USER_NAME, "", TEST_NEW_EMAIL)
        assert usr.get_user_email(TEST_USER_NAME) == TEST_NEW_EMAIL


def test_update_password(temp_user):
    TEST_NEW_PASSWORD = 'string'
    updated_dets = usr.update_fields(TEST_USER_NAME, TEST_NEW_PASSWORD, "")
    assert isinstance(updated_dets,dict)
    assert usr.get_user_password(TEST_USER_NAME) == TEST_NEW_PASSWORD


def test_update_password_fail(temp_user):
    with pytest.raises(ValueError):
        TEST_NEW_PASSWORD = '****'
        updated_dets = usr.update_fields(TEST_USER_NAME, TEST_NEW_PASSWORD, "")
        assert isinstance(updated_dets,dict)

def test_get_user_password(temp_user):
    assert usr.get_user_password(TEST_USER_NAME) is not None


def test_get_user_password_fail(temp_user):
    with pytest.raises(ValueError):
        assert usr.get_user_password(' ')


def test_update_email_and_password(temp_user):
    TEST_NEW_EMAIL = 'NEWSAMPLE@test.com'
    TEST_NEW_PASSWORD = 'NEWPASSWORD'
    updated_dets = usr.update_fields(TEST_USER_NAME, TEST_NEW_PASSWORD, TEST_NEW_EMAIL)
    assert isinstance(updated_dets,dict)
    assert usr.get_user_email(TEST_USER_NAME) == TEST_NEW_EMAIL
    assert "Password" in updated_dets["message"]


def test_update_email_and_password_fail(temp_user):
    with pytest.raises(ValueError):
        TEST_NEW_PASSWORD = 'NEWPASSWORD'
        usr.update_fields(TEST_USER_NAME, TEST_NEW_PASSWORD, "")
        updated_dets = usr.update_fields(TEST_USER_NAME, TEST_NEW_PASSWORD, "sampleuser@gmail.com")
        assert isinstance(updated_dets,dict)


def test_get_user(temp_user):
    assert usr.get_user(TEST_USER_NAME) is not None


def test_get_user_fail():
    with pytest.raises(ValueError):
        usr.get_user("fakeUser")


def test_update_username(temp_user):
    NEW_USERNAME = 'abc123'
    usr.update_username(TEST_USER_NAME, NEW_USERNAME)
    assert usr.user_exists(NEW_USERNAME)
    usr.del_user(NEW_USERNAME)


def test_update_username_fail_space(temp_user):
    if not RUNNING_ON_CICD_SERVER:
        NEW_USERNAME = ' '
        with pytest.raises(ValueError):
            usr.update_username(TEST_USER_NAME, NEW_USERNAME)


def test_update_username_fail_dupe(temp_user):
    if not RUNNING_ON_CICD_SERVER:
        with pytest.raises(ValueError):
            usr.update_username(TEST_USER_NAME, TEST_USER_NAME)


def test_update_username_fail_type(temp_user):
    if not RUNNING_ON_CICD_SERVER:
        NEW_USERNAME = 111
        with pytest.raises(TypeError):
            usr.update_username(TEST_USER_NAME, NEW_USERNAME)


def test_update_username_fail(temp_user):
    if not RUNNING_ON_CICD_SERVER:
        NEW_USERNAME1 = ''
        NEW_USERNAME2 = 'new user'
        with pytest.raises(ValueError):
            usr.update_username(TEST_USER_NAME, NEW_USERNAME1)
            usr.update_username(TEST_USER_NAME, NEW_USERNAME2)


def test_update_password(temp_user):
    TEST_NEW_PASSWORD = 'abc123'
    try:
        usr.update_fields(TEST_USER_NAME, TEST_NEW_PASSWORD, NEW_USER_DET['email'])
    except Exception as e:
        pytest.fail()


def test_update_password_fail(temp_user):
    TEST_NEW_PASSWORD1 = 'a'
    TEST_NEW_PASSWORD2 = 'a'
    with pytest.raises(ValueError):
        usr.update_fields(TEST_USER_NAME, TEST_NEW_PASSWORD1, "")
        usr.update_fields(TEST_USER_NAME, TEST_NEW_PASSWORD2, "")


def test_update_password_fail_type(temp_user):
    TEST_NEW_PASSWORD = 123
    with pytest.raises(TypeError):
        usr.update_fields(TEST_USER_NAME, TEST_NEW_PASSWORD, "")


def test_add_coin(temp_user_coin):
    usr.add_coin(TEST_USER_NAME, TEST_COIN)
    assert usr.user_coin_exists(TEST_USER_NAME, TEST_COIN)
    usr.remove_coin(TEST_USER_NAME, TEST_COIN)


def test_user_coin_evaluation(temp_user_coin):
    usr.add_coin(TEST_USER_NAME, TEST_COIN)
    assert usr.user_coin_valuation(TEST_USER_NAME) >= 0
    usr.remove_coin(TEST_USER_NAME, TEST_COIN)


def test_profile_add_post(temp_user):
    res = usr.profile_add_post(TEST_USER_NAME, TEST_TITLE, TEST_CONTENT, TEST_TAGS)
    assert res['posts'] is not None


def test_profile_add_post_fail(temp_user):
    with pytest.raises(ValueError):
        res = usr.profile_add_post(TEST_USER_NAME, "", "", "")


@pytest.mark.skip(reason="Require remove post to work")
def test_profile_remove_post(temp_user):
    assert usr.profile_delete_post(TEST_USER_NAME, 0)


@pytest.mark.skip(reason="Require change post to work")
def test_modify_posts(temp_user):
    # should include post number
    post_number = 0
    assert usr.user_profile_change_post(TEST_USER_NAME, post_number)


def test_user_login(temp_user3):
    assert usr.user_login(TEST_USER_NAME3, '****')


def test_user_login_fail(temp_user):
    with pytest.raises(Exception) as e:
        usr.user_login(TEST_USER_NAME, 'WRONGPASSWORD')


def test_get_coins(temp_user):
    assert isinstance(usr.get_coins(TEST_USER_NAME), list)


def test_get_followers(temp_user):
    assert isinstance(usr.get_followers(TEST_USER_NAME), list)


def test_get_followings(temp_user):
    assert isinstance(usr.get_followings(TEST_USER_NAME), list)


def test_get_all_posts_with_term(temp_user):
    assert isinstance(usr.get_all_posts("term"), list)


@patch('db.user_types.parse_list', return_value=[])
def test_get_no_posts_with_term(mock_user_details):
    usr.add_user(TEST_USER_NAME, NEW_USER_DET)
    lst = usr.get_all_posts("term")
    assert isinstance(lst, list)
    assert len(lst)==0
    if (usr.user_exists(TEST_USER_NAME)):
        usr.del_user(TEST_USER_NAME)


def test_get_all_posts(temp_user):
    assert isinstance(usr.get_all_posts(""), list)


@patch('db.db_connect.fetch_all', return_value=[])
def test_get_all_posts_no_users(mock_user_details):
    with pytest.raises(Exception):
        posts = usr.get_all_posts("term")
        assert isinstance(posts, list)