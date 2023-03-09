import os
import pytest
import db.coins as cn

TEST_COIN = 'TEST_COIN'
TEST_COIN_TICKER = 'TCN'
TEST_COIN_DETS = {'id': 3, 'name': TEST_COIN, 'symbol': TEST_COIN_TICKER,
                  'price': 1000}
INVALID_SYMBOL = '123'
VALID_SYMBOL = "NCM"
RUNNING_ON_CICD_SERVER = os.environ.get('CI', False)


@pytest.fixture(scope='function')
def temp_coin():
    # cn.testing_clear()
    cn.save_coin(TEST_COIN, TEST_COIN_DETS)
    yield
    cn.remove_coin(TEST_COIN)


def test_coinapi_setup():
    dets = cn.coinapi_setup()
    assert isinstance(dets, list)


def test_coinapi_setup_empty():
    dets = cn.coinapi_setup()
    assert len(dets) == 0


# @pytest.mark.skip(reason="Require additional func to check valid symbol")
def test_coinapi_price():
    newPrice = cn.coinapi_price(VALID_SYMBOL)
    assert isinstance(newPrice,float)


def test_coin_exists(temp_coin):
    assert cn.coin_exists(TEST_COIN)


def test_coin_exists_fail():
    INVAID_COIN = 'INVALID_COIN'
    assert not cn.coin_exists(INVAID_COIN)


def test_coin_details(temp_coin):
    if not RUNNING_ON_CICD_SERVER:
        coin_dets = cn.coin_details(TEST_COIN)
        assert isinstance(coin_dets, dict)


def test_coin_details_fail():
    with pytest.raises(ValueError):
        INVALID_COIN = 'INVALID_COIN'
        cn.coin_details(INVALID_COIN)


def test_get_coins():
    coins = cn.get_coins()
    assert isinstance(coins, list)


def test_count_coins():
    num = cn.count_coins()
    assert isinstance(num, int)


def test_get_coin_ticker(temp_coin):
    ticker = cn.get_coin_ticker(TEST_COIN)
    assert ticker == TEST_COIN_TICKER


def test_remodel_coin_ticker(temp_coin):
    if not RUNNING_ON_CICD_SERVER:
        remodel_symbol = "NEW"
        cn.remodel_coin_ticker(TEST_COIN, remodel_symbol)
        coin_symbol = cn.get_coin_ticker(TEST_COIN)
        cn.remodel_coin_ticker(TEST_COIN, TEST_COIN_TICKER)
        assert coin_symbol == remodel_symbol


def test_get_all_coin_tickers(temp_coin):
    tickers = cn.get_all_coin_tickers()
    assert isinstance(tickers, list)
    assert len(tickers) > 0


def test_coin_price(temp_coin):
    price = cn.coin_price(TEST_COIN)
    assert price == TEST_COIN_DETS['price']


def test_update_price(temp_coin):
    # using coin stored in db
    # cn.save_coin(TEST_COIN, TEST_COIN_DETS)
    coin = cn.update_price(TEST_COIN_TICKER)
    # cn.remove_coin(TEST_COIN)
    assert isinstance(coin,dict)


def test_update_price_fail():
    with pytest.raises(ValueError):
        coin = cn.update_price(INVALID_SYMBOL)