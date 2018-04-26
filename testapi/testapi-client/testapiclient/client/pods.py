import json

from testapiclient.client import base
from testapiclient.utils import urlparse


class PodsClient(base.Client):
    resource = 'pods'

    def __init__(self, **kwargs):
        super(PodsClient, self).__init__(**kwargs)

    def create(self, pod_req):
        return self.clientmanager.post(self.url, pod_req)

    def get(self):
        return json.dumps(self.clientmanager.get(self.url)['pods'])

    def get_one(self, name):
        return json.dumps(self.clientmanager.get(
            urlparse.path_join(self.url, name)))

    def delete(self, name):
        return self.clientmanager.delete(
            urlparse.path_join(self.url, name))
