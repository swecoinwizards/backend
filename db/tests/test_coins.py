import os
import pytest
import db.coins as cn

TEST_COIN = 'Ethereum'
TEST_COIN_TICKER = 'ETH'
TEST_COIN_DETS = {'id': 3, 'name': TEST_COIN, 'symbol': TEST_COIN_TICKER,
                  'price': 1282.32}
RUNNING_ON_CICD_SERVER = os.environ.get('CI', False)


@pytest.fixture(scope='function')
def temp_coin():
    cn.save_coin(TEST_COIN, TEST_COIN_DETS)
    yield
    cn.remove_coin(TEST_COIN)


def test_coinapi_setup():
    # cn.coinapi_setup()
    # assert isinstance(cn.coin_type, dict)
    # since data will be stored in db
    # api key will not be needed later on
    return True


def test_coin_exists(temp_coin):
    assert cn.coin_exists(TEST_COIN)


def test_coin_details(temp_coin):
    if not RUNNING_ON_CICD_SERVER:
        coin_dets = cn.coin_details(TEST_COIN)
        assert isinstance(coin_dets, dict)


def test_get_coins():
    coins = cn.get_coins()
    assert isinstance(coins, list)
    assert len(coins) > 1


def test_get_coins_dict():
    coins = cn.get_coin_dict()
    assert isinstance(coins, dict)


# test
def test_count_coins():
    num = cn.count_coins()
    assert num == 2


def test_get_coin_ticker(temp_coin):
    if not RUNNING_ON_CICD_SERVER:
        ticker = cn.get_coin_ticker(TEST_COIN)
        assert ticker == TEST_COIN_TICKER


def test_remodel_coin_ticker(temp_coin):
    if not RUNNING_ON_CICD_SERVER:
        remodel_symbol = "NEW"
        cn.remodel_coin_ticker(TEST_COIN, remodel_symbol)
        assert cn.get_coin_ticker(TEST_COIN) == remodel_symbol


def test_get_all_coin_tickers():
    tickers = cn.get_all_coin_tickers()
    assert isinstance(tickers, list)
    assert len(tickers) > 0


def test_coint_price():
    assert cn.coin_price('Bitcoin') == 20237.84301693455


def test_change_coin_price():
    new_price = cn.change_coin_price('Litecoin', 62.06)
    assert new_price == 62.06
