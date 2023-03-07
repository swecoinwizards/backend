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

users = Namespace(USERS_NS, 'Character Types')
api.add_namespace(users)
coins = Namespace(COINS_NS, 'Coins Type')
api.add_namespace(coins)

LIST = 'list'
DETAILS = 'details'
ADD = 'add'
REMOVE = 'remove'
UPDATE = 'update'
MAIN_MENU = '/main_menu'
MAIN_MENU_NM = 'Main Menu'
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
USER_UPDATE_EMAIL = f'/{DETAILS}/{UPDATE}/{EMAIL}'
USER_LOGIN = f'/{LOGIN}'
USER_LOGIN_MN = f'/{USERS_NS}'
USER_UPDATE_PASSWORD = f'/{DETAILS}/{UPDATE}/{PASSWORD}'
USER_POSTS = f'/{POSTS}'

COIN_LIST = f'/{LIST}'
COIN_LIST_NM = f'{COINS_NS}_list'
COIN_TICKERS_LIST = f'/{TICKERS}/{LIST}'
COIN_TICKERS_LIST_NM = f'{COINS_NS}_{TICKERS}_list'
COIN_DETAILS = f'/{DETAILS}'
COIN_REMOVE = f'{COINS_NS}/{REMOVE}'
COIN_FOLLOW = f'/{COINS_NS}/{FOLLOW}'
COIN_REMOVE_FOLLOW = f'/{COIN_REMOVE}/{FOLLOW}'
COIN_UPDATE = f'{DETAILS}/price'

DICT = 'dict'
USER_DICT = f'/{DICT}'
COIN_DICT = f'/{DICT}'

user_fields = api.model('NewUser', {
    user.NAME: fields.String,
    user.PASSWORD: fields.String,
    user.EMAIL: fields.String,
})


user_update_email_fields = api.model('UpdateUserEmail', {
    user.NAME: fields.String,
    user.EMAIL: fields.String,
})


user_update_password_field = api.model('UpdateUserPassword', {
    user.NAME: fields.String,
    user.PASSWORD: fields.String,
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
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, username):
        """
        Returns details about a user.
        """
        if user.user_exists(username):
            return {'Data': {username: {"Name": user.get_user(username)}},
                    'Type': 'Data', 'Title': 'User Type Details'}
        else:
            raise wz.NotFound(f'{user} not found.')


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
    @api.response(HTTPStatus.NOT_MODIFIED.value, 'Not Modified')
    def get(self, userA, userB):
        """
        Make userA follow userB.
        """
        try:
            return user.add_following(userA, userB)
        except Exception as e:
            raise wz.NotFound(f'Cannot modify: {e}')


@users.route(f'{USER_REMOVE_FOLLOW}/<userA>/<userB>')
class UserRemoveFollow(Resource):
    """
    Remove a follow relationship between two users.
    """
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.NOT_MODIFIED.value, 'Not Modified')
    def get(self, userA, userB):
        """
        Make userA unfollow userB.
        """
        try:
            return user.remove_follow(userA, userB)
        except Exception as e:
            raise wz.NotFound(f'Cannot modify: {e}')


@users.route(USER_UPDATE_EMAIL)
class UserUpdateEmail(Resource):
    @api.expect(user_update_email_fields)
    @api.response(HTTPStatus.OK.value, 'Success')
    @api.response(HTTPStatus.NOT_MODIFIED.value, 'Not Modified')
    def put(self):
        """
        Update an existing user's email.
        """
        try:
            return user.update_email(request.json[user.NAME],
                                     request.json[user.EMAIL])
        except Exception as e:
            raise wz.BadRequest(e)


@users.route(f'{USER_UPDATE_PASSWORD}')
class UserUpdatePassword(Resource):
    @api.expect(user_update_password_field)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_MODIFIED, 'Not Modified')
    def put(self):
        """
        Update an existing user's password
        """
        print(f'{request.json=}')
        try:
            # Probably should authenticate old password first
            return user.update_password(request.json[user.NAME],
                                        request.json[user.PASSWORD])
        except Exception as e:
            raise wz.BadRequest(e)


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
        return {'Data': coin.get_coin_dict(),
                'Type': 'Data',
                'Title': 'Active Coins'}


@coins.route(f'{COIN_DETAILS}/<coinName>')
class CoinTypeDetails(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
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
    def get(self, coinSymbol):
        """
        Returns coin with updated price.
        """
        ct = coin.update_price(coinSymbol)
        if ct is not None:
            return {coinSymbol: ct}
        else:
            raise wz.NotFound(f'{coinSymbol} not found.')


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
        except Exception as e:
            raise wz.BadRequest(f'{e}')


@users.route(f'{COIN_REMOVE_FOLLOW}/<username>/<coin>')
class CoinRemoveFollow(Resource):
    """
    Removes a follow relationship between a user and coin.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Modified')
    def get(self, username, coin):
        """
        Make a user unfollow a coin.
        """
        try:
            return user.remove_coin(username, coin)
        except Exception as e:
            wz.BadRequest(e)


@users.route(f'{USER_LOGIN}/<username>/<password>')
class UserLogin(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.EXPECTATION_FAILED, 'Unsuccessful')
    def get(self, username, password):
        """
        User login authentication
        """
        try:
            return {'Data': {username: user.user_login(username, password)},
                    'Type': 'Data',
                    'Title': 'User Login'}
        except Exception as e:
            return {'Data': f"Cannot login: {e}",
                    'Type': 'Form',
                    'Title': 'User Login'}


@users.route(f'{USER_FOLLOWERS}/<username>')
class UserFollowers(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.EXPECTATION_FAILED, 'Unsuccessful')
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
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.EXPECTATION_FAILED, 'Unsuccessful')
    def get(self, username):
        """
        Return a list of a user's followings.
        """
        try:
            return {'Data': {username:
                    {"followers": user.get_followings(username)}},
                    'Type': 'Data',
                    'Title': 'User Followings'}
        except Exception as e:
            return {'Data': f"Error: {e}",
                    'Type': 'Form',
                    'Title': 'User Followings'}


@users.route(f'{USER_POSTS}/<username>')
class UserPosts(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
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
