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


app = Flask(__name__)
api = Api(app)

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
LOGIN = 'login'
TICKERS = 'tickers'
POSTS = 'posts'
EMAIL = 'email'
PASSWORD = 'password'
# USERS_NS = 'users'
USER_LIST = f'/{LIST}'
USER_LIST_NM = f'{USERS_NS}_list'
USER_DETAILS = f'/{DETAILS}'
USER_ADD = f'/{ADD}'
USER_REMOVE = f'/{REMOVE}'
USER_FOLLOW = f'/{FOLLOW}'
USER_FOLLOWERS = f'/{FOLLOWERS}'
USER_REMOVE_FOLLOW = f'/{REMOVE}/{FOLLOW}'
USER_UPDATE_EMAIL = f'/{DETAILS}/{UPDATE}/{EMAIL}'
USER_LOGIN = f'/{LOGIN}'
USER_LOGIN_MN = f'/{USERS_NS}'
USER_UPDATE_PASSWORD = f'/{DETAILS}/{UPDATE}/{PASSWORD}'
USER_POSTS = f'/{POSTS}'
# COINS_NS = 'coins'
COIN_LIST = f'/{LIST}'
COIN_LIST_NM = f'{COINS_NS}_list'
COIN_TICKERS_LIST = f'/{TICKERS}/{LIST}'
COIN_TICKERS_LIST_NM = f'{COINS_NS}_{TICKERS}_list'
COIN_DETAILS = f'/{DETAILS}'
COIN_REMOVE = f'{COINS_NS}/{REMOVE}'
COIN_FOLLOW = f'/{COINS_NS}/{FOLLOW}'
COIN_REMOVE_FOLLOW = f'/{COIN_REMOVE}/{FOLLOW}'

DICT = 'dict'
USER_DICT = f'/{DICT}'
COIN_DICT = f'/{DICT}'


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
        Gets the main game menu.
        """
        return {'Title': MAIN_MENU_NM,
                'Default': 1,
                'Choices': {
                    '1': {'url': f'/{USER_DICT}',
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
    """
    This will get a list of currrent users.
    """
    def get(self):
        """
        Returns a list of current users.
        """
        data = user.get_users()
        print(data)
        return {USER_LIST_NM: data}


@users.route(USER_DICT)
class ActiveUsers(Resource):
    """
    FOR MENU
    This will get a list of currrent users in db.
    """
    def get(self):
        """
        Returns a list of current users.
        """
        return {'Data': user.get_users_dict(),
                'Type': 'Data',
                'Title': 'Active Users'}


@users.route(f'{USER_DETAILS}/<user_type>')
class UserTypeDetails(Resource):
    """
    For Menu
    This will return details on user.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, user_type):
        """
        Details on user.
        """
        print("here")
        if user.user_exists(user_type):
            print("here2")
            return {'Data': {user_type: {"Name": user.get_user(user_type)}},
                    'Type': 'Data', 'Title': 'User Type Details'}
        else:
            raise wz.NotFound(f'{user_type} not found.')


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


@users.route(USER_ADD)
class AddUser(Resource):
    """
    Add a user.
    """
    @api.expect(user_fields)
    def post(self):
        """
        Add a user.
        """
        print(f'{request.json=}')
        name = request.json[user.NAME]
        try:
            return user.add_user(name, request.json)
        except Exception as e:
            raise wz.BadRequest(f'{e}')


@users.route(f'{USER_REMOVE}/<user_type>')
class UserRemove(Resource):
    """
    Remove User
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, user_type):
        """
        This will return details on a character type
        """
        try:
            # does not remove user existence in other users
            return user.del_user(user_type)
        except Exception:
            raise wz.NotFound(f'{user_type} not found.')


@users.route(f'{USER_FOLLOW}/<user_type>/<user_type2>')
class UserFollow(Resource):
    """
    Follow User
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_MODIFIED, 'Not Modified')
    def get(self, user_type, user_type2):
        """
        Make one user follow another
        """
        try:
            return user.add_follower(user_type, user_type2)
        except Exception as e:
            raise wz.NotFound(f'Cannot modify: {e}')


@users.route(f'{USER_REMOVE_FOLLOW}/<user_type>/<user_type2>')
class UserRemoveFollow(Resource):
    """
    Remove follow
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_MODIFIED, 'Not Modified')
    def get(self, user_type, user_type2):
        """
        Add a user.
        """
        try:
            return user.remove_follower(user_type, user_type2)
        except Exception as e:
            raise wz.NotFound(f'Cannot modify: {e}')


@users.route(USER_UPDATE_EMAIL)
class UserUpdateEmail(Resource):
    """
    Update a user's email
    """
    @api.expect(user_update_email_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_MODIFIED, 'Not Modified')
    def put(self):
        """
        Update email
        """
        print(f'{request.json=}')
        print(user_update_email_fields)
        try:
            return user.update_email(request.json[user.NAME],
                                     request.json[user.EMAIL])
        except Exception as e:
            raise wz.BadRequest(e)


@users.route(f'{USER_UPDATE_PASSWORD}')
class UserUpdatePassword(Resource):
    """
    Update a user's password
    """
    @api.expect(user_update_password_field)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_MODIFIED, 'Not Modified')
    def put(self):
        """
        Update password
        """
        print(f'{request.json=}')
        try:
            return user.update_password(request.json[user.NAME],
                                        request.json[user.PASSWORD])
        except Exception as e:
            raise wz.BadRequest(e)


@coins.route(COIN_LIST)
class CoinList(Resource):
    """
    This will get a list of names of current coins.
    """
    def get(self):
        """
        Returns a list of full names of current coins
        """
        return {COIN_LIST_NM: coin.get_coins()}


@coins.route(COIN_TICKERS_LIST)
class CoinTickersList(Resource):
    """
    This will get a list of the tickers associated with current coins
    """
    def get(self):
        """
        Returns a list of coin tickers
        """
        return {COIN_TICKERS_LIST_NM: coin.get_all_coin_tickers()}


@coins.route(COIN_DICT)
class CoinsDict(Resource):
    """
    This will get a list of currrent coins in database.
    """
    def get(self):
        """
        Returns a detailed list of coins in the database.
        """
        return {'Data': coin.get_coin_dict(),
                'Type': 'Data',
                'Title': 'Active Coins'}


@coins.route(f'{COIN_DETAILS}/<coin_type>')
class CoinTypeDetails(Resource):
    """
    This will return details on a coin given the full coin name.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, coin_type):
        """
        Returns details of a coin given the full coin name.
        """
        ct = coin.coin_details(coin_type)
        if ct is not None:
            return {coin_type: ct}
        else:
            raise wz.NotFound(f'{coin_type} not found.')


@users.route(f'{COIN_FOLLOW}/<user_type>/<coin_type>')
class CoinFollow(Resource):
    """
    Follow Coin
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Modified')
    def get(self, user_type, coin_type):
        """
        Make a user follow a coin
        """
        print("SUCCESS")
        if (not coin.coin_exists(coin_type)):
            raise wz.NotFound(f'{coin_type} not found.')
        elif (not user.user_exists(user_type)):
            raise wz.NotAcceptable("User does not exists")
        elif (user.user_coin_exists(user_type, coin_type)):
            raise wz.NotAcceptable("Already following coin")
        else:
            return user.add_coin(user_type, coin_type)


@users.route(f'{COIN_REMOVE_FOLLOW}/<user_type>/<coin_type>')
class CoinRemoveFollow(Resource):
    """
    Remove follow
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Modified')
    def get(self, user_type, coin_type):
        """
        Remove coin from user
        """
        if (not user.user_exists(user_type)):
            raise wz.NotAcceptable("User does not exists")
        elif (not user.user_coin_exists(user_type, coin_type)):
            raise wz.NotAcceptable("Not following coin")
        else:
            return user.remove_coin(user_type, coin_type)


@users.route(f'{USER_LOGIN}/<username>/<password>')
class UserLogin(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.EXPECTATION_FAILED, 'Unsuccessful')
    def get(self, username, password):
        """
        Login
        """
        try:
            """
            Login to user
            """
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
        Get a list of people who follows the given user
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


# @users.route(f'{USER_POSTS}/<user_type>')
# class UserPosts(Resource):
#     @api.response(HTTPStatus.OK, 'Success')
#     @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
#     def get(self, user_type):
#         """
#         This will return details on a user post.
#         """
#         posts = user.get_posts(user_type)
#         if posts is not None:
#             return {'Data': {'Posts:': posts},
#                     'Type': 'Data', 'Title': 'Post History'}
#         else:
#             raise wz.NotFound(f'{user_type} not found.')


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
