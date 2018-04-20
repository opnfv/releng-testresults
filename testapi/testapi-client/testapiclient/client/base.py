from testapiclient.utils import clientmanager
from testapiclient.utils import urlparse


class AuthOption(object):
    def __init__(self, user=None, password=None):
        self.u = user
        self.p = password


class BaseClient(object):

    resource = ''

    def __init__(self, user=None, password=None, client_manager=None):
        self.url = urlparse.resource_join(self.resource)
        if client_manager:
            self.clientmanager = client_manager
        else:
            self.clientmanager = clientmanager.ClientManager(
                AuthOption(user, password))
            if self.clientmanager.auth_required:
                self.clientmanager.auth()
