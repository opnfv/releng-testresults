import requests
from user import User
from config import Config
import urllib
import functools


def do_authenticate(username, password):
    session = requests.Session()
    hostname = '{}{}{}'.format(
        Config.config.get("cas", "auth_url"),
        urllib.quote(Config.config.get("api", "url")),
        Config.config.get("cas", "signin_return"))
    data = {'name': username, 'pass': password, 'form_id': 'user_login'}
    response = session.post(hostname, data)
    User.session = session
    return response


def authenticate(xstep):
    @functools.wraps(xstep)
    def wrapper(self, parsed_args):
        username = parsed_args.u
        password = parsed_args.p
        if(username and password):
            response = do_authenticate(username, password)
            if "login" in response.text:
                print "Authentication has failed."
            else:
                xstep(self, parsed_args)
    return wrapper
