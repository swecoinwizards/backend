import pytest
import db.db_connect as dbc

TEST_DB = dbc.USER_DB
TEST_COLLECT = 'test_collect'
TEST_NAME = 'test'


def test_connect_db():
    dbc.connect_db()
    assert dbc.client is not None


@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT].insert_one({TEST_NAME: TEST_NAME})
    # yield to our test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT].delete_one({TEST_NAME: TEST_NAME})
