import json

from mock import mock
from six.moves.urllib import parse

from testapiclient.cli import scenarios
from testapiclient.tests.unit import fakes
from testapiclient.tests.unit import utils
from testapiclient.utils import clientmanager


class InstallerTest(utils.TestCommand):
    def setUp(self):
        super(InstallerTest, self).setUp()
        self.base_url = parse.urljoin(self.api_url, 'scenarios/{}/installers')
        self.scenario_name = 's1'
        self.installer_json = {
            'versions': [],
            'installer': 'test-installer',
        }
        self.installer_string = json.dumps(self.installer_json)


class InstallerCreateTest(InstallerTest):

    def setUp(self):
        super(InstallerCreateTest, self).setUp()

    def test_create_success(self):
        self.post_mock.return_value = fakes.FakeResponse(data=None)
        installer_create = scenarios.InstallerCreate(self.app, mock.Mock())
        args = ['--scenario-name', 's1', self.installer_string]
        verifies = [
            ('scenario_name', 's1'),
            ('installer', self.installer_json)]
        parsed_args = self.check_parser(installer_create, args, verifies)
        installer_create.take_action(parsed_args)
        self.post_mock.assert_called_once()


class InstallerDeleteTest(InstallerTest):

    def setUp(self):
        super(InstallerDeleteTest, self).setUp()

    def test_delete_success(self):
        self.delete_mock.return_value = fakes.FakeResponse(data=None)
        installer_delete = scenarios.InstallerDelete(self.app, mock.Mock())
        args = ['--scenario-name', 's1', 'def']
        verifies = [('scenario_name', 's1'), ('name', ['def'])]
        parsed_args = self.check_parser(installer_delete, args, verifies)
        installer_delete.take_action(parsed_args)
        self.delete_mock.assert_called_once_with(
            self.base_url.format(parsed_args.scenario_name),
            data=json.dumps(['def']),
            headers=clientmanager.ClientManager.headers)


class InstallerPutTest(InstallerTest):

    def setUp(self):
        super(InstallerPutTest, self).setUp()

    def test_put_success(self):
        self.put_mock.return_value = fakes.FakeResponse(
            data=None)
        installer_put = scenarios.InstallerPut(self.app, mock.Mock())
        args = ['--scenario-name', 's1', self.installer_string]
        verifies = [
            ('scenario_name', 's1'),
            ('installer', self.installer_json)]
        parsed_args = self.check_parser(installer_put, args, verifies)
        installer_put.take_action(parsed_args)
        self.put_mock.assert_called_once()
