
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
