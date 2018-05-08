import json

from six.moves.urllib import parse
import testtools

from testapiclient.client import projects
from testapiclient.tests.unit import fakes
from testapiclient.tests.unit import utils
from testapiclient.utils import clientmanager


class ProjectClientTest(utils.TestCommand):
    def setUp(self):
        super(ProjectClientTest, self).setUp()
        self.base_url = parse.urljoin(self.api_url, 'projects')
        self.project_json = {
            'description': 'test_description',
            'name': 'test_project',
        }
        self.project_client = projects.ProjectsClient()
        self.project_string = json.dumps(self.project_json)


class ProjectClientGetTest(ProjectClientTest):

    def setUp(self):
        super(ProjectClientGetTest, self).setUp()
        self.projects_rsp = {'projects': [self.project_json]}

    def test_get(self):
        self.get_mock.return_value = fakes.FakeResponse(
            data=self.projects_rsp)
        self.project_client.get()
        self.get_mock.assert_called_once_with(
            self.base_url,
            headers=clientmanager.ClientManager.headers)

    def test_get_search(self):
        self.get_mock.return_value = fakes.FakeResponse(
            data=self.projects_rsp)
        self.project_client.get(name='project1')
        self.get_mock.assert_called_once_with(
            self.base_url + '?name=project1',
            headers=clientmanager.ClientManager.headers)

    def test_get_one(self):
        self.get_mock.return_value = fakes.FakeResponse(
            data=self.project_json)
        self.project_client.get_one('def')
        self.get_mock.assert_called_once_with(
            self.base_url + '/def',
            headers=clientmanager.ClientManager.headers)


class ProjectClientCreateTest(ProjectClientTest):

    def setUp(self):
        super(ProjectClientCreateTest, self).setUp()
        self.succ_rsp = {
            'href': '{}/{}'.format(
                self.base_url, self.project_json.get('name'))
        }

    def test_create_success(self):
        self.post_mock.return_value = fakes.FakeResponse(
            data=self.succ_rsp)
        self.project_client.create(self.project_json)
        self.post_mock.assert_called_once()

    def test_create_failure(self):
        with testtools.ExpectedException(Exception, 'Create failed: Error'):
            self.post_mock.return_value = utils.FAKE_FAILURE
            self.project_client.create(self.project_json)


class ProjectClientDeleteTest(ProjectClientTest):

    def setUp(self):
        super(ProjectClientDeleteTest, self).setUp()

    def test_delete_success(self):
        self.delete_mock.return_value = fakes.FakeResponse()
        self.project_client.delete('def')
        self.delete_mock.assert_called_once_with(
            self.base_url + '/def',
            data=None,
            headers=clientmanager.ClientManager.headers)

    def test_delete_failure(self):
        with testtools.ExpectedException(Exception, 'Delete failed: Error'):
            self.delete_mock.return_value = utils.FAKE_FAILURE
            self.project_client.delete('def')


class ProjectClientUpdateTest(ProjectClientTest):

    def setUp(self):
        super(ProjectClientUpdateTest, self).setUp()

    def test_update_success(self):
        self.put_mock.return_value = fakes.FakeResponse()
        self.project_client.update('def', self.project_json)
        self.put_mock.assert_called_once_with(
            self.base_url + '/def',
            data=self.project_string,
            headers=clientmanager.ClientManager.headers)

    def test_update_failure(self):
        with testtools.ExpectedException(Exception, 'Update failed: Error'):
            self.put_mock.return_value = utils.FAKE_FAILURE
            self.project_client.update('def', self.project_json)
