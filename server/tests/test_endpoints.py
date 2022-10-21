
import pytest

import server.endpoints as ep
import db.user_types as user

TEST_CLIENT = ep.app.test_client()


SAMPLE_USER_NM = 'SampleUser'
SAMPLE_USER = {
    user.NAME: SAMPLE_USER_NM,
    user.FOLLOWERS: 10,
    user.FOLLOWING: 10,
}


def test_hello():
    """
    See if Hello works.
    """
    resp_json = TEST_CLIENT.get(ep.HELLO).get_json()
    assert isinstance(resp_json[ep.MESSAGE], str)


def test_add_user():
    """
    Test adding a user.
    """
    # print("pls work ", SAMPLE_USER.keys())
    resp = TEST_CLIENT.post(ep.USER_ADD, json=SAMPLE_USER)
    assert user.user_exists(SAMPLE_USER_NM)
    user.del_user(SAMPLE_USER_NM)


def test_get_user_list():
    """
    See if we can get a user list properly.
    Return should look like:
        {USER_LIST_NM: [list of users types...]}
    """
    resp = TEST_CLIENT.get(ep.USER_LIST)
    resp_json = resp.get_json()
    assert isinstance(resp_json[ep.USER_LIST_NM], list)



