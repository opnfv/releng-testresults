import json

from mock import mock
from six.moves.urllib import parse
import testtools

from testapiclient.cli import scenarios
from testapiclient.tests.unit import fakes as fk
from testapiclient.tests.unit import utils
from testapiclient.utils import clientmanager


class ScenarioTest(utils.TestCommand):
    def setUp(self):
        super(ScenarioTest, self).setUp()
        self.base_url = parse.urljoin(self.api_url, 'scenarios')
        self.scenario_json = {
            "installers": [],
            "name": "test_scenario"
        }
        self.scenario_string = json.dumps(self.scenario_json)


class ScenarioGetTest(ScenarioTest):

    def setUp(self):
        super(ScenarioGetTest, self).setUp()
        self.scenarios_rsp = {'scenarios': [self.scenario_json]}

    def test_get(self):
        self.get_mock.return_value = fk.FakeResponse(data=self.scenarios_rsp)
        scenario_get = scenarios.ScenarioGet(self.app, mock.Mock())
        args = ['-name', 's1', '-installer',
                'i1', '---version', 'v1', '-project', 'p1']
        verifies = [
            ('name', 's1'),
            ('installer', 'i1'),
            ('version', 'v1'),
            ('project', 'p1')]
        parsed_args = self.check_parser(scenario_get, args, verifies)
        scenario_get.take_action(parsed_args)
        kall = self.get_mock.call_args
        args, kwargs = kall
        self.assert_url(
            args[0],
            self.base_url + '?version=v1&name=s1&installer=i1&project=p1')

    def test_get_all(self):
        self.get_mock.return_value = fk.FakeResponse(data=self.scenarios_rsp)
        scenario_get = scenarios.ScenarioGet(self.app, mock.Mock())
        args = []
        verifies = []
        parsed_args = self.check_parser(scenario_get, args, verifies)
        scenario_get.take_action(parsed_args)
        self.get_mock.assert_called_once_with(
            self.base_url,
            headers=clientmanager.ClientManager.headers)

    def test_get_one(self):
        self.get_mock.return_value = fk.FakeResponse(data=self.scenario_json)
        scenario_get_one = scenarios.ScenarioGetOne(self.app, mock.Mock())
        args = ['def']
        verifies = [('name', 'def')]
        parsed_args = self.check_parser(scenario_get_one, args, verifies)
        scenario_get_one.take_action(parsed_args)
        self.get_mock.assert_called_once_with(
            self.base_url + '/def',
            headers=clientmanager.ClientManager.headers)


class ScenarioCreateTest(ScenarioTest):

    def setUp(self):
        super(ScenarioCreateTest, self).setUp()

    def test_create_success(self):
        succ_rsp = {
            'href': '{}/{}'.format(self.base_url,
                                   self.scenario_json.get('name'))
        }
        self.post_mock.return_value = fk.FakeResponse(data=succ_rsp)
        scenario_create = scenarios.ScenarioCreate(self.app, mock.Mock())
        args = [self.scenario_string]
        verifies = [('scenario', self.scenario_json)]
        parsed_args = self.check_parser(scenario_create, args, verifies)
        scenario_create.take_action(parsed_args)
        self.post_mock.assert_called_once()

    def test_create_failure(self):
        with testtools.ExpectedException(Exception, 'Create failed: Error'):
            self.post_mock.return_value = utils.FAKE_FAILURE
            scenario_create = scenarios.ScenarioCreate(self.app, mock.Mock())
            args = [self.scenario_string]
            verifies = [('scenario', self.scenario_json)]
            parsed_args = self.check_parser(scenario_create, args, verifies)
            scenario_create.take_action(parsed_args)


class ScenarioDeleteTest(ScenarioTest):

    def setUp(self):
        super(ScenarioDeleteTest, self).setUp()

    def test_delete_success(self):
        self.delete_mock.return_value = fk.FakeResponse()
        scenario_delete = scenarios.ScenarioDelete(self.app, mock.Mock())
        args = ['def']
        verifies = [('name', 'def')]
        parsed_args = self.check_parser(scenario_delete, args, verifies)
        scenario_delete.take_action(parsed_args)
        self.delete_mock.assert_called_once_with(
            self.base_url + '/def',
            data=None,
            headers=clientmanager.ClientManager.headers)

    def test_delete_failure(self):
        with testtools.ExpectedException(Exception, 'Delete failed: Error'):
            self.delete_mock.return_value = utils.FAKE_FAILURE
            scenario_delete = scenarios.ScenarioDelete(self.app, mock.Mock())
            args = ['def']
            verifies = [('name', 'def')]
            parsed_args = self.check_parser(scenario_delete, args, verifies)
            scenario_delete.take_action(parsed_args)


class ScenarioPutTest(ScenarioTest):

    def setUp(self):
        super(ScenarioPutTest, self).setUp()

    def test_put_success(self):
        self.put_mock.return_value = fk.FakeResponse(data=self.scenario_json)
        scenario_put = scenarios.ScenarioPut(self.app, mock.Mock())
        args = ['def', self.scenario_string]
        verifies = [('name', 'def'), ('scenario', self.scenario_json)]
        parsed_args = self.check_parser(scenario_put, args, verifies)
        scenario_put.take_action(parsed_args)
        self.put_mock.assert_called_once()

    def test_put_failure(self):
        with testtools.ExpectedException(Exception, 'Update failed: Error'):
            self.put_mock.return_value = utils.FAKE_FAILURE
            scenario_put = scenarios.ScenarioPut(self.app, mock.Mock())
            args = ['def', self.scenario_string]
            verifies = [('name', 'def'), ('scenario', self.scenario_json)]
            parsed_args = self.check_parser(scenario_put, args, verifies)
            scenario_put.take_action(parsed_args)
