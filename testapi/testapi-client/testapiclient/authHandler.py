import requests
from user import User
from config import Config
import urllib

class AuthHandler:

    @staticmethod
    def authenticate(username, password):
        session = requests.Session()
        hostname = Config.config.get(Config.mode, "auth_url") + urllib.quote(Config.config.get(Config.mode, "dev_api_url")) + Config.config.get(Config.mode, "signin_return")
        data = {'name': username, 'pass': password, 'form_id': 'user_login'}
        response = session.post(hostname, data)
        User.session = session
        return response
