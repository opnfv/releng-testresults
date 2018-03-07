import functools
import urllib

import requests

from testapiclient import config
from testapiclient import user


def _authenticate(username, password):
    session = requests.Session()
    hostname = '{}{}{}'.format(
        config.Config.config.get("cas", "auth_url"),
        urllib.quote(config.Config.config.get("api", "url")),
        config.Config.config.get("cas", "signin_return"))
    data = {'name': username, 'pass': password, 'form_id': 'user_login'}
    response = session.post(hostname, data)
    user.User.session = session
    return response


def authenticate(xstep):
    @functools.wraps(xstep)
    def wrapper(self, parsed_args):
        username = parsed_args.u
        password = parsed_args.p
        if(username and password):
            response = _authenticate(username, password)
            if "login" in response.text:
                print "Authentication has failed."
            else:
                xstep(self, parsed_args)
    return wrapper
