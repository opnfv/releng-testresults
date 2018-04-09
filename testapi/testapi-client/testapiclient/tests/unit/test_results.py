import json

from mock import mock
from six.moves.urllib import parse
import testtools

from testapiclient.cli import results
from testapiclient.tests.unit import fakes
from testapiclient.tests.unit import utils
from testapiclient.utils import clientmanager


class ResultTest(utils.TestCommand):
    def setUp(self):
        super(ResultTest, self).setUp()
        self.base_url = parse.urljoin(self.api_url, 'results')
        self.result_json = {
            'project_name': 'functest',
            'scenario': 'test-scenario',
            'stop_date': '2018-04-09 13:44:53',
            'case_name': 'test-case',
            'build_tag': 'test-build',
            'version': 'test-version',
            'pod_name': 'test-pod',
            'criteria': 'test-criteria',
            'installer': 'test-installer',
            'start_date': '2018-04-09 13:44:53',
            'details': 'test-details'
        }
        self.result_string = json.dumps(self.result_json)


class ResultGetTest(ResultTest):

    def setUp(self):
        super(ResultGetTest, self).setUp()
        self.results_rsp = {'results': [self.result_json]}

    def test_get(self):
        self.get_mock.return_value = fakes.FakeResponse(data=self.results_rsp)
        result_get = results.ResultGet(self.app, mock.Mock())
        args = ['-case', 'dfs']
        verifies = [('case', 'dfs')]
        parsed_args = self.check_parser(result_get, args, verifies)
        result_get.take_action(parsed_args)
        self.get_mock.assert_called_once_with(
            self.base_url + '?case=dfs',
            headers=clientmanager.ClientManager.headers)

    def test_get_all(self):
        self.get_mock.return_value = fakes.FakeResponse(data=self.results_rsp)
        result_get = results.ResultGet(self.app, mock.Mock())
        args = []
        verifies = []
        parsed_args = self.check_parser(result_get, args, verifies)
        result_get.take_action(parsed_args)
        self.get_mock.assert_called_once_with(
            self.base_url,
            headers=clientmanager.ClientManager.headers)

    def test_get_one(self):
        self.get_mock.return_value = fakes.FakeResponse(data=self.result_json)
        result_get_one = results.ResultGetOne(self.app, mock.Mock())
        args = ['def']
        verifies = [('result_id', 'def')]
        parsed_args = self.check_parser(result_get_one, args, verifies)
        result_get_one.take_action(parsed_args)
        self.get_mock.assert_called_once_with(
            self.base_url + '/def',
            headers=clientmanager.ClientManager.headers)


class ResultCreateTest(ResultTest):

    def setUp(self):
        super(ResultCreateTest, self).setUp()

    def test_create_success(self):
        succ_rsp = {
            'href': '{}/{}'.format(self.base_url,
                                   self.result_json.get('project_name'))
        }
        self.post_mock.return_value = fakes.FakeResponse(data=succ_rsp)
        result_create = results.ResultCreate(self.app, mock.Mock())
        args = [self.result_string]
        verifies = [('result', self.result_json)]
        parsed_args = self.check_parser(result_create, args, verifies)
        result_create.take_action(parsed_args)
        self.post_mock.assert_called_once()

    def test_create_failure(self):
        with testtools.ExpectedException(Exception, 'Create failed: Error'):
            self.post_mock.return_value = utils.FAKE_FAILURE
            result_create = results.ResultCreate(self.app, mock.Mock())
            args = [self.result_string]
            verifies = [('result', self.result_json)]
            parsed_args = self.check_parser(result_create, args, verifies)
            result_create.take_action(parsed_args)
