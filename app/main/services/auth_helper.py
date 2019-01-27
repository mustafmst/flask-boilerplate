from app.main.models.user import User
from app.main.services.blacklist_service import save_token


class Auth:

    @staticmethod
    def login_user(data):
        try:
            user: User = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    res = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
                    return res, 200
            else:
                res = {
                    'status': 'fail',
                    'message': 'email or password does not match'
                }
                return res, 401
        except Exception as e:
            print(e)
            res = {
                'status': 'fail',
                'message': 'Try again'
            }
            return res, 500

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(' ')[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                return save_token(token=auth_token)
            else:
                res = {
                    'status': 'fail',
                    'message': resp
                }
                return res, 401
        else:
            res = {
                'status': 'fail',
                'message': 'Provide a valid auth token'
            }
            return res, 403

