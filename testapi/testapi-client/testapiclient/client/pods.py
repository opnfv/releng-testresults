from testapiclient.client import base


class PodsClient(base.BaseClient):
    resource = 'pods'

    def __init__(self, **kwargs):
        super(PodsClient, self).__init__(**kwargs)

    def create(self, pod_req):
        self.clientmanager.post(self.url, pod_req)
