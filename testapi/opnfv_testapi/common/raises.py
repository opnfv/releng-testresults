##############################################################################
# Copyright (c) 2017 ZTE Corp
# feng.xiaowei@zte.com.cn
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import http.client

from tornado import web


class Raiser(object):
    code = http.client.OK

    def __init__(self, reason):
        raise web.HTTPError(self.code, reason=reason)


class BadRequest(Raiser):
    code = http.client.BAD_REQUEST


class Forbidden(Raiser):
    code = http.client.FORBIDDEN


class Conflict(Raiser):
    code = http.client.CONFLICT


class NotFound(Raiser):
    code = http.client.NOT_FOUND


class Unauthorized(Raiser):
    code = http.client.UNAUTHORIZED


class CodeTBD(object):
    def __init__(self, code, reason):
        raise web.HTTPError(code, reason)
