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
DESCRIPTION = 'description'
URLS = "urls"
LOGO = "logo"
TAGS = "tags"
DA = "dateAdded"
TEST_COIN = 'Bitcoin'
REQUIRED_FIELDS = [ID, NAME, SYMBOL, PRICE, DESCRIPTION, URLS, LOGO, TAGS, DA]
USE_TRUE = "1"
USE_FALSE = "0"


# helper function for inputting user data to db
def coin_dets_cleanUp(coin):
    if '_id' in coin:
        del coin['_id']
    return coin


def coinapi_setup(quotes=10):
    if os.environ.get("USE_CMC", USE_FALSE) == USE_TRUE:
        cmc = CoinMarketCapAPI(API_KEY)
        r = cmc.cryptocurrency_map()
        # only using first 10 coins for now
        temp_lst = []
        dbc.connect_db()
        for line in r.data[0:quotes]:
            quote = cmc.cryptocurrency_quotes_latest(symbol=line['symbol'])
            price = quote.data[line['symbol']][0]['quote']['USD']['price']
            coin_dets = cmc.cryptocurrency_info(symbol=line['symbol']).data
            description = coin_dets[line['symbol']][0]['description']
            urls = coin_dets[line['symbol']][0]['urls']
            logo = coin_dets[line['symbol']][0]['logo']
            tags = coin_dets[line['symbol']][0]['tags']
            dateAdded = coin_dets[line['symbol']][0]['date_added']
            if not coin_exists(line['name']):
                dets = {ID: line['id'], NAME: line['name'],
                        SYMBOL: line['symbol'], PRICE: price,
                        DESCRIPTION: description,
                        URLS: urls, LOGO: logo,
                        TAGS: tags, DA: dateAdded}
                temp_lst.append({NAME: line['name'],
                                SYMBOL: line['symbol'], PRICE: price,
                                DESCRIPTION: description,
                                URLS: urls, LOGO: logo,
                                TAGS: tags, DA: dateAdded})
                dbc.insert_one(COINS_COLLECT, dets, COIN_DB)
            else:
                dbc.update_one(COINS_COLLECT, {'symbol': line['symbol']},
                                              {'$set': {
                                                PRICE: price,
                                                DESCRIPTION: description,
                                                URLS: urls, LOGO: logo,
                                                TAGS: tags, DA: dateAdded}},
                               COIN_DB)
                temp_lst.append({NAME: line['name'],
                                SYMBOL: line['symbol'], PRICE: price,
                                DESCRIPTION: description,
                                URLS: urls, LOGO: logo,
                                TAGS: tags, DA: dateAdded})

        return temp_lst
    else:
        print("Did not fetch CoinMarketCap data.")
        return []


def get_latest_quotes(quotes=10):
    os.environ["USE_CMC"] = "1"
    coin_lst = coinapi_setup(int(quotes))
    os.environ["USE_CMC"] = "0"
    return coin_lst


def coinapi_price(symb):
    # Helper function for update_price
    if os.environ.get("USE_CMC", USE_FALSE) == USE_TRUE:
        cmc = CoinMarketCapAPI(API_KEY)
        # only using first 10 coins for now
        quote = cmc.cryptocurrency_quotes_latest(symbol=symb)
        price = quote.data[symb][0]['quote']['USD']['price']
        dbc.connect_db()
        dbc.update_one(COINS_COLLECT, {'symbol': symb}, {
            '$pull': {'price': price}}, COIN_DB)
        return price
    else:
        # return ValueError(f'Did not fetch new price for {symb}')
        return -1.0


def remove_coin(name):
    dbc.connect_db()
    if not coin_exists(name):
        raise ValueError(f'Coin: {name} does not exist!')
    dbc.remove_one(COINS_COLLECT, {"name": name}, COIN_DB)
    # del coin_type[name]
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
    return temp['symbol']


def remodel_coin_ticker(name, remodel_symbol):
    dbc.connect_db()
    temp = dbc.fetch_one(COINS_COLLECT, {"name": name}, COIN_DB)
    if temp is None:
        raise ValueError(f'Coin: {name} does not exist!')
    temp['symbol'] = remodel_symbol
    dbc.update_one(COINS_COLLECT, {'name': name}, {
            '$set': {'symbol': remodel_symbol}}, COIN_DB)
    return True


def get_all_coin_tickers():
    tickers = []
    dbc.connect_db()
    coins = dbc.fetch_all(COINS_COLLECT, COIN_DB)
    for coin in coins:
        tickers.append(coin['symbol'])
    return tickers


def save_coin(name, dets):
    if not isinstance(name, str):
        raise TypeError(f'Wrong type for name: {type(name)=}')
    if not isinstance(dets, dict):
        raise TypeError(f'Wrong type for coin details: {type(dets)=}')
    dbc.connect_db()
    if not coin_exists(name):
        dbc.insert_one(COINS_COLLECT, dets, COIN_DB)
    else:
        dbc.update_one(COINS_COLLECT, {'symbol': dets['symbol']},
                       {'$set': {
                                PRICE: dets['price'],
                                DESCRIPTION: dets['description'],
                                URLS: dets['urls'],
                                LOGO: dets['logo'],
                                TAGS: dets['tags'],
                                DA: dets['dateAdded']}}, COIN_DB)
    return True


def coin_market_api_request(coinName):
    # Coin name has to be lowercase
    cmc = CoinMarketCapAPI(API_KEY)
    # r = cmc.cryptocurrency_map()
    quote = cmc.cryptocurrency_info(slug=coinName.lower()).data
    for key in quote:
        coin_symbol = quote[key]['symbol']
        quote2 = cmc.cryptocurrency_quotes_latest(symbol=coin_symbol).data
    return [quote, quote2, coin_symbol, key]


def new_coin_details(coinName):
    dbc.connect_db()
    coin_dets = {}
    os.environ["USE_CMC"] = "1"
    api_request_dets = coin_market_api_request(coinName)
    if len(api_request_dets) == 0:
        raise ValueError("Did not fetch CoinMarketCap data.")
    os.environ["USE_CMC"] = "0"
    # quote, quote2, coin_symbol, key = coin_market_api_request(coinName)
    quote = api_request_dets[0]
    quote2 = api_request_dets[1]
    coin_symbol = api_request_dets[2]
    key = api_request_dets[3]
    for item in REQUIRED_FIELDS:
        if item == PRICE:
            coin_dets[item] = quote2[coin_symbol][0]["quote"]["USD"][item]
        elif item == DA:
            coin_dets[item] = quote2[coin_symbol][0]["date_added"]
        elif item in quote[key]:
            coin_dets[item] = quote[key][item]
        else:
            if item in [NAME, ID, SYMBOL, PRICE, DESCRIPTION, LOGO, DA]:
                coin_dets[item] = "Unavailable"
            else:
                coin_dets[item] = {}
    save_coin(coin_dets['name'], coin_dets)
    return coin_dets_cleanUp(coin_dets)
