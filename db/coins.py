import os
import db.db_connect as dbc
from coinmarketcapapi import CoinMarketCapAPI

# from config import API_KEY
# https://pypi.org/project/python-coinmarketcap/

API_KEY = os.environ.get("CMC_KEY")
COINS_COLLECT = 'coins'
COIN_DB = 'coindb'
ID = 'id'
NAME = 'name'
SYMBOL = 'symbol'
PRICE = 'price'
TEST_COIN = 'Bitcoin'
REQUIRED_FIELDS = [ID, NAME, SYMBOL, PRICE]
USE_TRUE = "1"
USE_FALSE = "0"

# database will use
coin_type = {'Bitcoin': {'id': 1, 'name': 'Bitcoin', 'symbol': 'BTC',
             'price': 20237.84301693455}, 'Litecoin': {'id': 2,
             'name': 'Litecoin', 'symbol': 'LTC', 'price': 62.885530866205976}}


def coinapi_setup():
    if os.environ.get("USE_CMC", USE_FALSE) == USE_TRUE:
        cmc = CoinMarketCapAPI(API_KEY)
        r = cmc.cryptocurrency_map()
        # only using first 10 coins for now
        temp_lst = []
        dbc.connect_db()
        for line in r.data[2:10]:
            quote = cmc.cryptocurrency_quotes_latest(symbol=line['symbol'])
            price = quote.data[line['symbol']][0]['quote']['USD']['price']
            print(price)
            if not coin_exists(line['name']):
                dets = {ID: line['id'], NAME: line['name'],
                        SYMBOL: line['symbol'], PRICE: price}
                temp_lst.append(dets)
                dbc.insert_one(COINS_COLLECT, dets, COIN_DB)
        return temp_lst
    else:
        print("Did not fetch CoinMarketCap data.")
        return []


def coinapi_price(symb):
    # Helper function for update_price
    if os.environ.get("USE_CMC", USE_FALSE) == USE_TRUE:
        cmc = CoinMarketCapAPI(API_KEY)
        # only using first 10 coins for now
        quote = cmc.cryptocurrency_quotes_latest(symbol=symb)
        price = quote.data[symb][0]['quote']['USD']['price']
        return price
    else:
        return ValueError(f'Did not fetch new price for {symb}')


def update_price(symbol):
    temp = dbc.fetch_one(COINS_COLLECT, {"symbol": symbol}, COIN_DB)
    if (temp is None):
        raise ValueError(f'Coin: {symbol} does not exist!')
    newPrice = coinapi_price(symbol)
    if (newPrice is False):
        return ValueError(f'Cannot get new price for {symbol}')
    temp["price"] = newPrice
    dbc.remove_one(COINS_COLLECT, {"symbol": symbol}, COIN_DB)
    dbc.insert_one(COINS_COLLECT, {"symbol": symbol}, COIN_DB)
    return temp


def save_coin(name, dets):
    if not isinstance(name, str):
        raise TypeError(f'Wrong type for name: {type(name)=}')
    if not isinstance(dets, dict):
        raise TypeError(f'Wrong type for coin details: {type(dets)=}')
    if coin_exists(name):
        raise ValueError("Coin with name %s already exists!", name)
    coin_type[name] = dets
    dbc.connect_db()
    dbc.insert_one(COINS_COLLECT, dets, COIN_DB)
    return True


def remove_coin(name):
    dbc.connect_db()
    if not coin_exists(name):
        raise ValueError(f'Coin: {name} does not exist!')
    dbc.remove_one(COINS_COLLECT, {"name": name}, COIN_DB)
    del coin_type[name]
    return True


def coin_exists(name):
    dbc.connect_db()
    temp = dbc.fetch_one(COINS_COLLECT, {"name": name}, COIN_DB)
    return temp is not None


def coin_details(name):
    dbc.connect_db()
    temp = dbc.fetch_one(COINS_COLLECT, {"name": name}, COIN_DB)
    if temp is None:
        raise ValueError(f'Coin: {name} does not exist!')
    return temp


def get_coins():
    dbc.connect_db()
    return dbc.fetch_all(COINS_COLLECT, COIN_DB)
    # return list(coin_type.keys())


def get_coin_dict():
    '''
    FOR MENU
    '''
    return coin_type


def count_coins():
    dbc.connect_db()
    return len(dbc.fetch_all(COINS_COLLECT, COIN_DB))


def coin_price(name):
    dbc.connect_db()
    temp = dbc.fetch_one(COINS_COLLECT, {"name": name}, COIN_DB)
    if temp is None:
        raise ValueError(f'Coin: {name} does not exist!')
    return temp['price']


def get_coin_ticker(name):
    dbc.connect_db()
    temp = dbc.fetch_one(COINS_COLLECT, {"name": name}, COIN_DB)
    if temp is None:
        raise ValueError(f'Coin: {name} does not exist!')
    return coin_type[name]['symbol']


def remodel_coin_ticker(name, remodel_symbol):
    coin_type[name]['symbol'] = remodel_symbol
    return True


def get_all_coin_tickers():
    tickers = []
    dbc.connect_db()
    coins = dbc.fetch_all(COINS_COLLECT, COIN_DB)
    for coin in coins:
        tickers.append(coin['symbol'])
    return tickers


def change_coin_price(name, new_price):
    coin_type[name]['price'] = new_price
    return coin_type[name]['price']


def main():
    coinapi_setup()
