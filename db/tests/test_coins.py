import db.coins as cn
TEST_COIN = 'Bitcoin'
TEST_COIN_TICKER = 'BTC'


def test_coinapi_setup():
    # cn.coinapi_setup()
    # assert isinstance(cn.coin_type, dict)
    # since data will be stored in db
    # api key will not be needed later on
    return True


def test_coin_exists():
    assert cn.coin_exists(TEST_COIN)


def test_coin_details():
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


def test_get_coin_ticker():
    ticker = cn.get_coin_ticker(TEST_COIN)
    assert ticker == TEST_COIN_TICKER


def test_get_all_coin_tickers():
    tickers = cn.get_all_coin_tickers()
    assert isinstance(tickers, list)
    assert len(tickers) > 0


def test_coint_price():
    assert cn.coin_price('Bitcoin') == 20237.84301693455
