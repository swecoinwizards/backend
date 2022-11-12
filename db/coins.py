from coinmarketcapapi import CoinMarketCapAPI
# from config import API_KEY
# https://pypi.org/project/python-coinmarketcap/

API_KEY = ''
ID = 'id'
NAME = 'name'
SYMBOL = 'symbol'
PRICE = 'price'
TEST_COIN = 'Bitcoin'
REQUIRED_FIELDS = [ID, NAME, SYMBOL, PRICE]

# database will use
coin_type = {'Bitcoin': {'id': 1, 'name': 'Bitcoin', 'symbol': 'BTC',
             'price': 20237.84301693455}, 'Litecoin': {'id': 2,
             'name': 'Litecoin', 'symbol': 'LTC', 'price': 62.885530866205976}}


# should save to a database in the future
def coinapi_setup():
    cmc = CoinMarketCapAPI(API_KEY)
    r = cmc.cryptocurrency_map()
    # only using first 10 coins for now
    for line in r.data[2:10]:
        # metaData = cmc.cryptocurrency_info(id = line['id']) - INCLUDES
        # DESCRIPTION metaData.data['description'], metaData.data['logo']
        # print(metaData.data)
        quote = cmc.cryptocurrency_quotes_latest(symbol=line['symbol'])
        price = quote.data[line['symbol']]['quote']['USD']['price']
        coin_type[line['name']] = {ID: line['id'], NAME: line['name'],
                                   SYMBOL: line['symbol'], PRICE: price}
    # print(coin_type)


def coin_exists(name):
    return name in coin_type


def coin_details(name):
    if name not in coin_type:
        raise ValueError(f'User {name=} not added yet')
    return coin_type[name]


def get_coins():
    return list(coin_type.keys())


def get_coin_dict():
    '''
    FOR MENU
    '''
    return coin_type


def count_coins():
    return len(coin_type.keys())


def coin_price(name):
    return coin_type[name]['price']


def main():
    coinapi_setup()
    print(coin_type)
