# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import httplib
import unittest
import jwt
import datetime

from tornado import web

from opnfv_testapi.common import message
from opnfv_testapi.tests.unit import executor
from opnfv_testapi.tests.unit import fake_pymongo
from opnfv_testapi.tests.unit.handlers import test_result


class TestTokenCreateResult(test_result.TestResultBase):
    def get_app(self):
        from opnfv_testapi.router import url_mappings
        return web.Application(
            url_mappings.mappings,
            db=fake_pymongo,
            debug=True,
            auth=True
        )

    @executor.mock_valid_lfid()
    def setUp(self):
        super(TestTokenCreateResult, self).setUp()
        self.current_time = datetime.datetime.utcnow()
        self.time_extend = datetime.timedelta(seconds=10000)
        self.token = jwt.encode(
            {
                'user': self.user,
                'a': {2: True},
                'exp': self.time_extend + self.current_time
            },
            'replace_it', algorithm='HS256'
            )

    @executor.mock_valid_lfid()
    @executor.create(httplib.FORBIDDEN, message.invalid_token())
    def test_resultCreateTokenInvalid(self):
        self.headers['X-Auth-Token'] = 'fdfsfsf'
        return self.req_d

    @executor.mock_valid_lfid()
    @executor.create(httplib.UNAUTHORIZED, message.unauthorized())
    def test_resultCreateTokenUnauthorized(self):
        if 'X-Auth-Token' in self.headers:
            self.headers.pop('X-Auth-Token')
        return self.req_d

    @executor.mock_valid_lfid()
    @executor.create(httplib.OK, '_create_success')
    def test_resultCreateTokenSuccess(self):
        self.headers['X-Auth-Token'] = self.token
        return self.req_d

    def _create_success(self, body):
        self.assertIn('CreateResponse', str(type(body)))


if __name__ == '__main__':
    unittest.main()
