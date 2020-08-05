from base.handler.base_handler import tornado_wrap, BaseHandler
from database.user import DbUser

import log


class LoginHandler(BaseHandler):
    @staticmethod
    def failed_resp():
        return {
            'code': 60204,
            'message': 'Account and password are incorrect.'
        }

    @staticmethod
    def success_resp(token):
        return {
            'code': 20000,
            'data': {'token': token},
        }

    @tornado_wrap
    async def post(self, params, data, headers):
        username, password = data.get('username'), data.get('password')

        if None in (username, password):
            return 200, self.failed_resp()

        user = await DbUser.get_user(username, password)
        if user is None:
            return 200, self.failed_resp()

        token = user.token

        return 200, self.success_resp(token)


class UserInfoHandler(BaseHandler):
    @staticmethod
    def failed_resp():
        return {
            'code': 50008,
            'message': 'Login failed, unable to get user details.'
        }

    @staticmethod
    def success_resp(user: DbUser):
        return {
            'code': 20000,
            'data': {
                'roles': user.roles.split(' '),
                'introduction': user.introduction,
                'avatar': user.avatar,
                'name': user.name
            },
        }

    @tornado_wrap
    async def get(self, params, data, headers):
        token = params.get('token')
        user = await DbUser.get_user_by_token(token)

        if user is None:
            return 200, self.failed_resp()

        resp = self.success_resp(user)
        return 200, resp
