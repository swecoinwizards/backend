"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from flask import Flask, request
from flask_restx import Resource, Api, fields, Namespace
from db import user_types as user
from db import coins as coin
import werkzeug.exceptions as wz
from http import HTTPStatus

API_DOC = '/api/doc'
API_PFX = '/api'

app = Flask(__name__)
api = Api(app, doc='/api/doc', prefix='/api')

USERS_NS = 'users'
COINS_NS = 'coins'

users = Namespace(USERS_NS, 'Users Type')
api.add_namespace(users)
coins = Namespace(COINS_NS, 'Coins Type')
api.add_namespace(coins)

LIST = 'list'
DETAILS = 'details'
EXIST = 'exist'
ADD = 'add'
REMOVE = 'remove'
UPDATE = 'update'
MAIN_MENU = '/main_menu'
MAIN_MENU_NM = 'Main Menu'
OPTIONS = '/options'
HELLO = '/hello'
MESSAGE = 'message'
FOLLOW = 'follow'
FOLLOWERS = 'followers'
FOLLOWINGS = 'followings'
LOGIN = 'login'
TICKERS = 'tickers'
POSTS = 'posts'
EMAIL = 'email'
PASSWORD = 'password'
USER_LIST = f'/{LIST}'
USER_LIST_NM = f'{USERS_NS}_list'
USER_DETAILS = f'/{DETAILS}'
USER_ADD = f'/{ADD}'
REMOVE_USER = f'/{REMOVE}'
USER_FOLLOW = f'/{FOLLOW}'
USER_FOLLOWERS = f'/{FOLLOWERS}'
USER_FOLLOWINGS = f'/{FOLLOWINGS}'
USER_REMOVE_FOLLOW = f'/{REMOVE}/{FOLLOW}'
USER_UPDATE = f'/{DETAILS}/{UPDATE}'
USER_LOGIN = f'/{LOGIN}'
USER_LOGIN_MN = f'/{USERS_NS}'
USER_POSTS = f'/{POSTS}'

COIN_LIST = f'/{LIST}'
COIN_LIST_NM = f'{COINS_NS}_list'
COIN_TICKERS_LIST = f'/{TICKERS}/{LIST}'
COIN_TICKERS_LIST_NM = f'{COINS_NS}_{TICKERS}_list'
COIN_DETAILS = f'/{DETAILS}'
COIN_REMOVE = f'{COINS_NS}/{REMOVE}'
COIN_FOLLOW = f'/{COINS_NS}/{FOLLOW}'
COIN_REMOVE_FOLLOW = f'/{COIN_REMOVE}/{FOLLOW}'
COIN_UPDATE = f'/{DETAILS}/price'
COIN_EXISTS = f'/{COINS_NS}/{EXIST}'

DICT = 'dict'
USER_DICT = f'/{DICT}'
COIN_DICT = f'/{DICT}'

USER_UPDATE_DOC = {
    "description": "Not all fields required; leave blank if not updating"
}

user_fields = api.model('NewUser', {
    user.NAME: fields.String,
    user.PASSWORD: fields.String,
    user.EMAIL: fields.String,
})

user_update_fields = api.model('UpdateUser', {
    'new_password': fields.String(default='', required=False),
    'new_email': fields.String(default='', required=False),
})


@api.route(HELLO)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {MESSAGE: 'hello world'}


@api.route(MAIN_MENU)
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main menu.
        """
        return {'Title': MAIN_MENU_NM,
                'Default': 1,
                'Choices': {
                    '1': {'url': f'/{USER_LIST}',
                          'method': 'get', 'text': 'List Active Users'},
                    '2': {'url': f'/{COIN_DICT}',
                          'method': 'get', 'text': 'List Active Coins'},
                    '3': {'url': f'{USER_LOGIN}/Investor/****',
                          'method': 'get', 'text': 'User Investor Login'},
                    '4': {'url': f'{USER_FOLLOWERS}/Investor',
                          'method': 'get', 'text': 'User Investor Followers'},
                    '5': {'url': f'{USER_DETAILS}/Investor',
                          'method': 'get', 'text': 'User Investor Details'},
                    'X': {'text': 'Exit'},
                }}


@api.route(OPTIONS)
class OptionsMenu(Resource):
    """
    This will deliver our options menu.
    """
    def get(self):
        """
        Gets the main menu.
        """
        return {'Title': "Options Menu",
                'Default': 1,
                'Choices': [
                    {"value": "users_list", "label": "users"},
                    {"value": "coins_list", "label": "coins"},
                    {"value": "posts_list", "label": "posts"}
                ]}


@users.route(USER_LIST)
class UserList(Resource):
    def get(self):
        """
        Returns a list of current users.
        """
        data = user.get_users()
        return {USER_LIST_NM: data}


@users.route(f'{USER_DETAILS}/<username>')
class UserDetails(Resource):
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST.value, 'Bad Request')
    def get(self, username):
        """
        Returns details about a user.
        """
        try:
            return {'Data': {username: {"Name": user.get_user(username)}},
                    'Type': 'Data', 'Title': 'User Type Details'}
        except Exception as e:
            raise wz.BadRequest(f'Could not fetch user: {e}')


@users.route(USER_ADD)
class AddUser(Resource):
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.CONFLICT.value, 'Conflict')
    @api.expect(user_fields)
    def post(self):
        """
        Add a new user.
        """
        print(f'{request.json=}')
        name = request.json[user.NAME]
        try:
            return user.add_user(name, request.json)
        except Exception as e:
            raise wz.Conflict(f'{e}')


@users.route(f'{REMOVE_USER}/<username>')
class RemoveUser(Resource):
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.NOT_FOUND.value, 'Not Found')
    @api.expect(user_fields)
    def get(self, username):
        """
        Remove an existing user.
        """
        try:
            # does not remove user existence in other users
            return user.del_user(username)
        except Exception:
            raise wz.NotFound(f'{username} not found.')


@users.route(f'{USER_FOLLOW}/<userA>/<userB>')
class UserFollow(Resource):
    """
    Create follow relationship between two users.
    """
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST.value, 'Bad Request')
    def get(self, userA, userB):
        """
        Make userA follow userB.
        """
        try:
            return user.add_following(userA, userB)
        except Exception as e:
            raise wz.BadRequest(f'Cannot modify: {e}')


@users.route(f'{USER_REMOVE_FOLLOW}/<userA>/<userB>')
class UserRemoveFollow(Resource):
    """
    Remove a follow relationship between two users.
    """
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST.value, 'Bad Request')
    def get(self, userA, userB):
        """
        Make userA unfollow userB.
        """
        try:
            return user.remove_follow(userA, userB)
        except Exception as e:
            raise wz.BadRequest(f'Cannot modify: {e}')


@users.route(f'{USER_UPDATE}/<username>', doc=USER_UPDATE_DOC)
class UserUpdate(Resource):
    @api.expect(user_update_fields)
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST.value, 'Bad Request')
    def put(self, username):
        """
        Update a user's details.
        """
        try:
            new_password = request.json['new_password']
            new_email = request.json['new_email']

            return user.update_fields(username, new_password, new_email)
        except Exception as e:
            raise wz.BadRequest(f'Update failed: {e}')


@coins.route(COIN_LIST)
class CoinList(Resource):
    def get(self):
        """
        Returns a list of full names of current coins.
        """
        return {COIN_LIST_NM: coin.get_coins()}


@coins.route(COIN_TICKERS_LIST)
class CoinTickersList(Resource):
    def get(self):
        """
        Returns a list of existing coin tickers.
        """
        return {COIN_TICKERS_LIST_NM: coin.get_all_coin_tickers()}


@coins.route(COIN_DICT)
class CoinsDict(Resource):
    def get(self):
        """
        Returns a detailed list of coins in the database.
        """
        return {'Data': coin.get_coins(),
                'Type': 'Data',
                'Title': 'Active Coins'}


@coins.route(f'{COIN_DETAILS}/<coinName>')
class CoinTypeDetails(Resource):
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.NOT_FOUND.value, 'Not Found')
    def get(self, coinName):
        """
        Returns details of a coin given the coin name.
        """
        ct = coin.coin_details(coinName)
        if ct is not None:
            return {coinName: ct}
        else:
            raise wz.NotFound(f'{coinName} not found.')


@coins.route(f'{COIN_UPDATE}/<coinSymbol>')
class CoinPriceUpdate(Resource):
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST.value, 'Bad Request')
    def get(self, coinSymbol):
        """
        Returns coin with updated price.
        """
        try:
            ct = coin.update_price(coinSymbol)
            return {coinSymbol: ct}
        except Exception as e:
            raise wz.BadRequest(f'{e}')


@coins.route(f'{COIN_LIST}/{UPDATE}/<numer_quotes>')
class GetLatestCoins(Resource):
    def get(self, numer_quotes):
        """
        Returns # of quotes from coinmarket api
        """
        ct = coin.get_latest_quotes(numer_quotes)
        return ct


@users.route(f'{COIN_EXISTS}/<username>/<coin>')
class CoinExists(Resource):
    """
    Check if user follows coin
    """
    @api.response(HTTPStatus.OK.value, 'Success')
    def get(self, username, coin):
        return user.user_coin_exists(username, coin)


@users.route(f'{COIN_FOLLOW}/<username>/<coin>')
class CoinFollow(Resource):
    """
    Adds a follow relationship between a user and coin.
    """
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST.value, 'Bad Request')
    def get(self, username, coin):
        """
        Make a user follow a coin.
        """
        try:
            return user.add_coin(username, coin)
        except ValueError as e:
            raise wz.BadRequest(f'{e}')


@users.route(f'{COIN_REMOVE_FOLLOW}/<username>/<coin>')
class CoinRemoveFollow(Resource):
    """
    Removes a follow relationship between a user and coin.
    """
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE.value, 'Not Modified')
    def get(self, username, coin):
        """
        Make a user unfollow a coin.
        """
        try:
            return user.remove_coin(username, coin)
        except Exception as e:
            raise wz.BadRequest(f'Error {e}')


@users.route(f'{USER_LOGIN}/<username>/<password>')
class UserLogin(Resource):
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.UNAUTHORIZED.value, 'Unauthorized')
    def get(self, username, password):
        """
        User login authentication
        """
        try:
            return user.user_login(username, password)
        except Exception as e:
            raise wz.Unauthorized(f'{e}')


@users.route(f'{USER_FOLLOWERS}/<username>')
class UserFollowers(Resource):
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.EXPECTATION_FAILED.value, 'Unsuccessful')
    def get(self, username):
        """
        Return a list of a user's followers.
        """
        try:
            return {'Data': {username:
                    {"followers": user.get_followers(username)}},
                    'Type': 'Data',
                    'Title': 'User Followers'}
        except Exception as e:
            return {'Data': f"Error: {e}",
                    'Type': 'Form',
                    'Title': 'User Followers'}


@users.route(f'{USER_FOLLOWINGS}/<username>')
class UserFollowings(Resource):
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.EXPECTATION_FAILED.value, 'Unsuccessful')
    def get(self, username):
        """
        Return a list of a user's followings.
        """
        try:
            return {'Data': {username:
                    {"followings": user.get_followings(username)}},
                    'Type': 'Data',
                    'Title': 'User Followings'}
        except Exception as e:
            return {'Data': f"Error: {e}",
                    'Type': 'Form',
                    'Title': 'User Followings'}


@users.route(f'{USER_POSTS}/<username>')
class UserPosts(Resource):
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.NOT_FOUND.value, 'Not Found')
    def get(self, username):
        """
        Returns a list of a user's posts.
        """
        posts = user.get_posts(username)
        if posts is not None:
            return {'Data': {'Posts:': posts},
                    'Type': 'Data', 'Title': 'Post History'}
        else:
            raise wz.NotFound(f'{username} not found.')


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = ''
        # sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}
