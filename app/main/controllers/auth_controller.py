from flask import request
from flask_restplus import Resource

from app.main.services.auth_helper import Auth
from app.main.utils.dto import AuthDto

api = AuthDto.api
_user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    @api.doc('user login')
    @api.expect(_user_auth, validate=True)
    def post(self):
        post_data = request.json
        return Auth.login_user(post_data)


@api.route('/logout')
class UserLogout(Resource):
    @api.doc('logout user')
    def post(self):
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(auth_header)
