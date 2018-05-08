import json

from testapiclient.client import base
from testapiclient.utils import urlparse


class ProjectsClient(base.Client):
    resource = 'projects'

    def __init__(self, **kwargs):
        super(ProjectsClient, self).__init__(**kwargs)

    def create(self, project_req):
        return self.clientmanager.post(self.url, project_req)

    def get(self, **queries):
        if queries:
            return json.dumps(
                self.clientmanager.get(
                    urlparse.query_join(self.url, **queries))['projects'])
        else:
            return json.dumps(
                self.clientmanager.get(self.url)['projects'])

    def get_one(self, name):
        return json.dumps(self.clientmanager.get(
            urlparse.path_join(self.url, name)))

    def delete(self, name):
        return self.clientmanager.delete(
            urlparse.path_join(self.url, name))

    def update(self, name, project_req):
        return self.clientmanager.put(
            urlparse.path_join(self.url, name), project_req)
