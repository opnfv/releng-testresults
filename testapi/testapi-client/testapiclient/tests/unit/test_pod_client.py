import json

from six.moves.urllib import parse
import testtools

from testapiclient.client import pods
from testapiclient.tests.unit import fakes
from testapiclient.tests.unit import utils
from testapiclient.utils import clientmanager


class PodClientTest(utils.TestCommand):
    def setUp(self):
        super(PodClientTest, self).setUp()
        self.base_url = parse.urljoin(self.api_url, 'pods')
        self.pod_json = {
            'role': 'community-ci',
            'name': 'test_pod',
            'details': '',
            'mode': 'metal'
        }
        self.pod_client = pods.PodsClient()
        self.pod_string = json.dumps(self.pod_json)


class PodClientGetTest(PodClientTest):

    def setUp(self):
        super(PodClientGetTest, self).setUp()
        self.pods_rsp = {'pods': [self.pod_json]}

    def test_get(self):
        self.get_mock.return_value = fakes.FakeResponse(data=self.pods_rsp)
        self.pod_client.get()
        self.get_mock.assert_called_once_with(
            self.base_url,
            headers=clientmanager.ClientManager.headers)

    def test_get_search(self):
        self.get_mock.return_value = fakes.FakeResponse(data=self.pods_rsp)
        self.pod_client.get(name='pod1')
        self.get_mock.assert_called_once_with(
            self.base_url + '?name=pod1',
            headers=clientmanager.ClientManager.headers)

    def test_get_one(self):
        self.get_mock.return_value = fakes.FakeResponse(data=self.pod_json)
        self.pod_client.get_one('def')
        self.get_mock.assert_called_once_with(
            self.base_url + '/def',
            headers=clientmanager.ClientManager.headers)


class PodClientCreateTest(PodClientTest):

    def setUp(self):
        super(PodClientCreateTest, self).setUp()
        self.succ_rsp = {
            'href': '{}/{}'.format(self.base_url, self.pod_json.get('name'))
        }

    def test_create_success(self):
        self.post_mock.return_value = fakes.FakeResponse(data=self.succ_rsp)
        self.pod_client.create(self.pod_json)
        self.post_mock.assert_called_once()

    def test_create_failure(self):
        with testtools.ExpectedException(Exception, 'Create failed: Error'):
            self.post_mock.return_value = utils.FAKE_FAILURE
            self.pod_client.create(self.pod_json)


class PodClientDeleteTest(PodClientTest):

    def setUp(self):
        super(PodClientDeleteTest, self).setUp()

    def test_delete_success(self):
        self.delete_mock.return_value = fakes.FakeResponse()
        self.pod_client.delete('def')
        self.delete_mock.assert_called_once_with(
            self.base_url + '/def',
            data=None,
            headers=clientmanager.ClientManager.headers)

    def test_delete_failure(self):
        with testtools.ExpectedException(Exception, 'Delete failed: Error'):
            self.delete_mock.return_value = utils.FAKE_FAILURE
            self.pod_client.delete('def')
