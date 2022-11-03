import db.coins as cn
TEST_COIN = 'Bitcoin'


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
