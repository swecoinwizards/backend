"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask, request
from flask_restx import Resource, Api, fields  # , Namespace
import db.user_types as user
import db.coins as coin
import werkzeug.exceptions as wz
from http import HTTPStatus


app = Flask(__name__)
api = Api(app)


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
USERS_NS = 'users'
USER_LIST = f'/{USERS_NS}/{LIST}'
USER_LIST_NM = f'{USERS_NS}_list'
USER_DETAILS = f'/{USERS_NS}/{DETAILS}'
USER_ADD = f'/{USERS_NS}/{ADD}'
USER_REMOVE = f'/{USERS_NS}/{REMOVE}'
USER_FOLLOW = f'/{USERS_NS}/{FOLLOW}'
USER_REMOVE_FOLLOW = f'/{USERS_NS}/{REMOVE}/{FOLLOW}'
USER_UPDATE_EMAIL = f'/{USERS_NS}/{DETAILS}/{UPDATE}'
COINS_NS = 'coins'
COIN_LIST = f'/{COINS_NS}/{LIST}'
COIN_LIST_NM = f'{COINS_NS}_list'
COIN_DETAILS = f'/{COINS_NS}/{DETAILS}'
COIN_REMOVE = f'/{COINS_NS}/{REMOVE}'
COIN_FOLLOW = f'/{USERS_NS}/{COINS_NS}/{FOLLOW}'
COIN_REMOVE_FOLLOW = f'/{USERS_NS}/{COINS_NS}/{REMOVE}/{FOLLOW}'

DICT = 'dict'
USER_DICT = f'/{DICT}'


# user_types = Namespace(USER_LIST_NM, 'Character Types')
# api.add_namespace(user_types)


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
                    '1': {'text': 'List User Types'},
                    '2': {'url': f'/{USER_DICT}',
                          'method': 'get', 'text': 'List Active Users'},
                    '3': {'url': '/coins/list',
                          'method': 'get', 'text': 'List Active Coins'},
                    'X': {'text': 'Exit'},
                }}


@api.route(USER_LIST)
class UserList(Resource):
    """
    This will get a list of currrent users.
    """
    def get(self):
        """
        Returns a list of current users.
        """
        return {USER_LIST_NM: user.get_users()}


@api.route(USER_DICT)
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


@api.route(f'{USER_DETAILS}/<user_type>')
class UserTypeDetails(Resource):
    """
    This will return details on a character type.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, user_type):
        """
        This will return details on a character type.
        """
        ct = user.get_user_type_details(user_type)
        if ct is not None:
            return {user_type: user.get_user_type_details(user_type)}
        else:
            raise wz.NotFound(f'{user_type} not found.')


user_fields = api.model('NewUser', {
    user.NAME: fields.String,
    user.PASSWORD: fields.String,
    user.EMAIL: fields.String,
    user.FOLLOWERS: fields.Integer,
    user.FOLLOWING: fields.Integer,
    user.COINS: fields.Integer,
})


user_update_email_fields = api.model('UpdateUserEmail', {
    user.NAME: fields.String,
    user.EMAIL: fields.String,
})


@api.route(USER_ADD)
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
        # del request.json[user.NAME]
        print(user_fields)
        user.add_user(name, request.json)


@api.route(f'{USER_REMOVE}/<user_type>')
class UserRemove(Resource):
    """
    Remove User
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, user_type):
        """
        This will return details on a character type.
        """
        ct = user.get_user_type_details(user_type)
        if ct is not None:
            return user.del_user(user_type)
        else:
            raise wz.NotFound(f'{user_type} not found.')


@api.route(f'{USER_FOLLOW}/<user_type>/<user_type2>')
class UserFollow(Resource):
    """
    Follow User
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_MODIFIED, 'Not Modified')
    def get(self, user_type, user_type2):
        """
        Add a user.
        """
        return user.add_follower(user_type, user_type2)


@api.route(f'{USER_REMOVE_FOLLOW}/<user_type>/<user_type2>')
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
        return user.remove_follower(user_type, user_type2)


@api.route(USER_UPDATE_EMAIL)
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
        return user.update_email(request.json[user.NAME],
                                 request.json[user.EMAIL])


@api.route(COIN_LIST)
class CoinList(Resource):
    """
    This will get a list of currrent users.
    """
    def get(self):
        """
        Returns a list of current users.
        """
        return {COIN_LIST_NM: coin.get_coins()}


@api.route(f'{COIN_DETAILS}/<coin_type>')
class CoinTypeDetails(Resource):
    """
    This will return details on a character type.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, coin_type):
        """
        This will return details on a character type.
        """
        ct = coin.coin_details(coin_type)
        if ct is not None:
            return {coin_type: ct}
        else:
            raise wz.NotFound(f'{coin_type} not found.')


@api.route(f'{COIN_FOLLOW}/<user_type>/<coin_type>')
class CoinFollow(Resource):
    """
    Follow Coin
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Modified')
    def get(self, user_type, coin_type):
        if (not coin.coin_exists(coin_type)):
            raise wz.NotFound(f'{coin_type} not found.')
        elif (not user.user_exists(user_type)):
            raise wz.NotAcceptable("User does not exists")
        elif (user.user_coin_exists(user_type, coin_type)):
            raise wz.NotAcceptable("Already following coin")
        else:
            return user.add_coin(user_type, coin_type)


@api.route(f'{COIN_REMOVE_FOLLOW}/<user_type>/<coin_type>')
class CoinRemoveFollow(Resource):
    """
    Remove follow
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Modified')
    def get(self, user_type, coin_type):
        if (not coin.coin_exists(coin_type)):
            raise wz.NotFound(f'{coin_type} not found.')
        elif (not user.user_exists(user_type)):
            raise wz.NotAcceptable("User does not exists")
        elif (not user.user_coin_exists(user_type, coin_type)):
            raise wz.NotAcceptable("Not following coin")
        else:
            return user.remove_coin(user_type, coin_type)


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
