from mock import mock

from testapiclient import main
from testapiclient.tests.unit import utils


class AppTest(utils.TestCommand):
    def setUp(self):
        super(AppTest, self).setUp()
        self.auth_post = mock.patch(
            'testapiclient.utils.clientmanager.ClientManager.auth').start()
        self.app = main.TestAPIClient()

    def test_auth_called(self):
        self.app.run(
            ['-u', 'thuva4', '-p', 'Ramanujam@007', 'pod', 'create',
             '{"name": "asfad"}'])
        self.auth_post.assert_called_once_with()

    def test_auth_not_called(self):
        self.app.run(['pod', 'get'])
        self.auth_post.assert_not_called()
