import json

from mock import mock
from six.moves.urllib import parse

from testapiclient.cli import scenarios
from testapiclient.tests.unit import fakes
from testapiclient.tests.unit import utils
from testapiclient.utils import clientmanager


class VersionTest(utils.TestCommand):
    def setUp(self):
        super(VersionTest, self).setUp()
        self.base_url = parse.urljoin(self.api_url, 'scenarios/{}/versions')
        self.scenario_name = 's1'
        self.version_json = {
            'projects': [],
            'version': 'test-version',
            'owner': 'test_owner'
        }
        self.version_string = json.dumps(self.version_json)


class VersionCreateTest(VersionTest):

    def setUp(self):
        super(VersionCreateTest, self).setUp()

    def test_create_success(self):
        self.post_mock.return_value = fakes.FakeResponse(data=None)
        version_create = scenarios.VersionCreate(self.app, mock.Mock())
        args = [
            '--scenario-name', 's1', '--installer', 'i1', self.version_string]
        verifies = [
            ('scenario_name', 's1'),
            ('installer', 'i1'),
            ('version', self.version_json)]
        parsed_args = self.check_parser(version_create, args, verifies)
        version_create.take_action(parsed_args)
        self.post_mock.assert_called_once()


class VersionDeleteTest(VersionTest):

    def setUp(self):
        super(VersionDeleteTest, self).setUp()

    def test_delete_success(self):
        self.delete_mock.return_value = fakes.FakeResponse(data=None)
        version_delete = scenarios.VersionDelete(self.app, mock.Mock())
        args = ['--scenario-name', 's1', '--installer', 'i1', 'def']
        verifies = [
            ('scenario_name', 's1'),
            ('installer', 'i1'),
            ('name', ['def'])]
        parsed_args = self.check_parser(version_delete, args, verifies)
        version_delete.take_action(parsed_args)
        self.delete_mock.assert_called_once_with(
            self.base_url.format(parsed_args.scenario_name) + '?installer=i1',
            data=json.dumps(['def']),
            headers=clientmanager.ClientManager.headers)


class VersionPutTest(VersionTest):

    def setUp(self):
        super(VersionPutTest, self).setUp()

    def test_put_success(self):
        self.put_mock.return_value = fakes.FakeResponse(
            data=None)
        version_put = scenarios.VersionPut(self.app, mock.Mock())
        args = [
            '--scenario-name', 's1', '--installer', 'i1', self.version_string]
        verifies = [
            ('scenario_name', 's1'),
            ('installer', 'i1'),
            ('version', self.version_json)]
        parsed_args = self.check_parser(version_put, args, verifies)
        version_put.take_action(parsed_args)
        self.put_mock.assert_called_once()


class VersionOwnerPutTest(VersionTest):

    def setUp(self):
        super(VersionOwnerPutTest, self).setUp()

    def test_put_success(self):
        self.put_mock.return_value = fakes.FakeResponse(
            data=None)
        version_put = scenarios.VersionOwnerPut(self.app, mock.Mock())
        version_owner = {
            'owner': 'test_owner'
        }
        args = [
            '--scenario-name', 's1', '--installer', 'i1',
            '--version', 'v1', json.dumps(version_owner)]
        verifies = [
            ('scenario_name', 's1'),
            ('installer', 'i1'),
            ('version', 'v1'),
            ('owner', version_owner)]
        parsed_args = self.check_parser(version_put, args, verifies)
        version_put.take_action(parsed_args)
        self.put_mock.assert_called_once()
