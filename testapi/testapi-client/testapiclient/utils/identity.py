import functools
import os
import urllib

import requests

from testapiclient.utils import user


def _authenticate(username, password):
    session = requests.Session()
    hostname = '{}{}{}'.format(os.environ.get('testapi_cas_auth_url'),
                               urllib.quote(os.environ.get('testapi_url')),
                               os.environ.get('testapi_cas_signin_return'))
    data = {
        'name': username,
        'pass': password,
        'form_id': 'user_login'
    }
    response = session.post(hostname, data)
    if "login" not in response.text:
        user.User.session = session
    return response


def authenticate(xstep):
    @functools.wraps(xstep)
    def wrapper(self, parsed_args):
        if(user.User.session is None):
            username = parsed_args.u
            password = parsed_args.p
            if(username and password):
                response = _authenticate(username, password)
                if "login" in response.text:
                    print "Authentication has failed."
                    return
        xstep(self, parsed_args)
    return wrapper
