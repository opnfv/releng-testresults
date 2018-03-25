import jwt
from tornado import gen
from tornado import web
import datetime


from opnfv_testapi.common import constants
from opnfv_testapi.common import raises
from opnfv_testapi.common.config import CONF
from opnfv_testapi.db import api as dbapi
from opnfv_testapi.handlers import base_handlers
from opnfv_testapi.models.user_models import User


class TokenHandler(base_handlers.GenericApiHandler):
    def __init__(self, application, request, **kwargs):
        super(TokenHandler, self).__init__(application, request, **kwargs)
        self.table_cls = User

    @web.asynchronous
    @gen.coroutine
    def get(self):
        current_time = datetime.datetime.utcnow()
        if CONF.api_authenticate:
            username = self.get_secure_cookie(constants.TESTAPI_ID)
            if username:
                user = yield dbapi.db_find_one('users', {'user': username})
                cls_data = self.table_cls.from_dict(user).format_http()
                time_extend = datetime.timedelta(seconds=1000)
                token = self.token_create(cls_data, current_time + time_extend)
                self.set_header('X-Auth-Token', token)
                self.finish()
            else:
                raises.Unauthorized('Unauthorized')
        else:
            time_extend = datetime.timedelta(seconds=10000)
            user_data = User(
                'anonymous',
                'anonymous@linuxfoundation.com',
                'anonymous lf',
                constants.TESTAPI_USERS).format()
            token = self.token_create(user_data, current_time + time_extend)
            self.set_header('X-Auth-Token', token)
            self.finish()

    def token_create(self, user_data, exp_time):
        token = jwt.encode(
            {
                'user': user_data,
                'a': {2: True},
                'exp': exp_time
            },
            CONF.api_secret, algorithm='HS256'
            )
        return token
