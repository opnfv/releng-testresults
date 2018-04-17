import urllib

from mock import mock

from testapiclient import main
from testapiclient.tests.unit import utils
from testapiclient.tests.unit import fakes


class MainTest(utils.TestCommand):
    def setUp(self):
        super(MainTest, self).setUp()
        self.app = main.TestAPIClient()

    def test_auth_success(self):
        self.post_mock.return_value = fakes.FakeResponse(
            data={'text': "success"})
        self.app.run(
            ['-u', 'test1', '-p', 'test2', 'pod', 'create',
             '{"name": "asfad"}'])
        self.post_mock.assert_called_with(
            'http://localhost:8000/api/v1/pods',
            data='{"name": "asfad"}',
            headers={
                'Content-type': 'application/json',
                'Accept': 'text/plain'})

    def test_auth_failure(self):
        self.post_mock.return_value = fakes.FakeResponse(
            data={'text': "login"})
        self.app.run(
            ['-u', 'test1', '-p', 'test2', 'pod', 'create',
             '{"name": "asfad"}'])
        hostname = '{}{}{}'.format(
            self.env_variables['testapi_cas_auth_url'],
            urllib.quote(self.env_variables['testapi_url']),
            self.env_variables['testapi_cas_signin_return'])
        self.post_mock.assert_called_with(
            hostname,
            {
                'pass': 'test2',
                'name': 'test1',
                'form_id': 'user_login'}
        )

    def test_auth_not_called(self):
        self.auth_post = mock.patch(
            'testapiclient.utils.clientmanager.ClientManager.auth').start()
        self.app.run(['pod', 'get'])
        self.auth_post.assert_not_called()
