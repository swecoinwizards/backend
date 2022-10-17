
import db.db as dbs


def test_get_accounts():
    acc_list = dbs.get_accounts()
    assert isinstance(acc_list, list)
    assert len(acc_list) > 0


def test_add_account():
    status = dbs.add_account()
    assert isinstance(status, bool)


def test_delete_account():
    status = dbs.delte_account()
    assert isinstance(status, bool)


def test_update_account():
    status = dbs.update_account()
    assert isinstance(status, bool)


def test_get_user_followers():
    followers = dbs.get_user_followers("test")
    assert isinstance(followers, list)


def test_get_user_following():
    following = dbs.get_user_following("test")
    assert isinstance(following, list)


def test_add_user_post():
    status = dbs.add_user_post("test")
    assert isinstance(status, bool)


def test_get_user_posts():
    posts = dbs.get_user_posts("test")
    assert isinstance(posts, list)
