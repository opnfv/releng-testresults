import requests
from user import User
from config import Config
import urllib


def authenticate(username, password):
    session = requests.Session()
    hostname = '{}{}{}'.format(
        Config.config.get("cas", "auth_url"),
        urllib.quote(Config.config.get("api", "url")),
        Config.config.get("cas", "signin_return"))
    data = {'name': username, 'pass': password, 'form_id': 'user_login'}
    response = session.post(hostname, data)
    User.session = session
    return response
