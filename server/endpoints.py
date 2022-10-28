"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask, request
from flask_restx import Resource, Api, fields  # , Namespace
import db.user_types as user
import werkzeug.exceptions as wz
from http import HTTPStatus


app = Flask(__name__)
api = Api(app)


LIST = 'list'
DETAILS = 'details'
ADD = 'add'
REMOVE = 'remove'
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
