import json
from argparse import Namespace
from six.moves.urllib import parse

import models
import utils.clientmanager

class TestApiWrapper(object):

    def __init__(self, user, password):
        self.options = Namespace(u=user, p=password)
        self.client_manager = utils.clientmanager.ClientManager(self.options)
        self.client_manager.auth()

    def _create(self, model, url):
        return self.client_manager.post(url, model.__dict__)

    def _update(self, model, url):
        return self.client_manager.put(url, model.__dict__)

    def _get(self, url):
        return self.client_manager.get(url)

    def _delete(self, url, *args):
        return self.client_manager.delete(url, *args)

class PodWrapper(TestApiWrapper):

    def __init__(self, user, password):
        super(PodWrapper, self).__init__(user, password)
        self.url="http://localhost:8000/api/v1/pods"

    def create_pod(self, pod):
        return self._create(pod, self.url)

    def update_pod(self, name, pod):
        return self._update(pod, parse.urljoin(self.url+"/", name))

    def get_all_pod(self):
        return self._get(self.url)

    def get_one_pod(self, name):
        return self._get(parse.urljoin(self.url+"/", name))


