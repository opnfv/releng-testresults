import json

from mock import mock
from six.moves.urllib import parse
import testtools

from testapiclient.cli import testcases
from testapiclient.tests.unit import fakes
from testapiclient.tests.unit import utils
from testapiclient.utils import clientmanager


class TestcaseTest(utils.TestCommand):
    def setUp(self):
        super(TestcaseTest, self).setUp()
        self.base_url = parse.urljoin(self.api_url, 'projects/{}/cases')
        self.project_name = 'functest'
        self.testcase_json = {
            'run': '',
            'name': 'test-case',
            'ci_loop': '',
            'tags': '',
            'url': '',
            'blocking': '',
            'domains': '',
            'dependencies': '',
            'version': '',
            'criteria': '',
            'tier': '',
            'trust': '',
            'catalog_description': '',
            'description': ''
        }
        self.testcase_string = json.dumps(self.testcase_json)


class TestcaseGetTest(TestcaseTest):

    def setUp(self):
        super(TestcaseGetTest, self).setUp()
        self.testcases_rsp = {'testcases': [self.testcase_json]}

    def test_get(self):
        self.get_mock.return_value = fakes.FakeResponse(
            data=self.testcases_rsp)
        testcase_get = testcases.TestcaseGet(self.app, mock.Mock())
        args = ['--project-name', 'dfs']
        verifies = [('project_name', 'dfs')]
        parsed_args = self.check_parser(testcase_get, args, verifies)
        testcase_get.take_action(parsed_args)
        self.get_mock.assert_called_once_with(
            self.base_url.format(parsed_args.project_name),
            headers=clientmanager.ClientManager.headers)

    def test_get_one(self):
        self.get_mock.return_value = fakes.FakeResponse(
            data=self.testcase_json)
        testcase_get_one = testcases.TestcaseGetOne(self.app, mock.Mock())
        args = ['--project-name', 'functest', 'def']
        verifies = [('project_name', 'functest'), ('name', 'def')]
        parsed_args = self.check_parser(testcase_get_one, args, verifies)
        testcase_get_one.take_action(parsed_args)
        self.get_mock.assert_called_once_with(
            self.base_url.format(parsed_args.project_name) + '/def',
            headers=clientmanager.ClientManager.headers)


class TestcaseCreateTest(TestcaseTest):

    def setUp(self):
        super(TestcaseCreateTest, self).setUp()

    def test_create_success(self):
        succ_rsp = {
            'href': '{}/{}'.format(self.base_url.format(self.project_name),
                                   self.testcase_json.get('name'))
        }
        self.post_mock.return_value = fakes.FakeResponse(data=succ_rsp)
        testcase_create = testcases.TestcaseCreate(self.app, mock.Mock())
        args = ['--project-name', 'functest', self.testcase_string]
        verifies = [
            ('project_name', 'functest'),
            ('testcase', self.testcase_json)]
        parsed_args = self.check_parser(testcase_create, args, verifies)
        testcase_create.take_action(parsed_args)
        self.post_mock.assert_called_once()

    def test_create_failure(self):
        with testtools.ExpectedException(Exception, 'Create failed: Error'):
            self.post_mock.return_value = utils.FAKE_FAILURE
            testcase_create = testcases.TestcaseCreate(self.app, mock.Mock())
            args = ['--project-name', 'functest', self.testcase_string]
            verifies = [
                ('project_name', 'functest'),
                ('testcase', self.testcase_json)]
            parsed_args = self.check_parser(testcase_create, args, verifies)
            testcase_create.take_action(parsed_args)


class TestcaseDeleteTest(TestcaseTest):

    def setUp(self):
        super(TestcaseDeleteTest, self).setUp()

    def test_delete_success(self):
        self.delete_mock.return_value = fakes.FakeResponse()
        testcase_delete = testcases.TestcaseDelete(self.app, mock.Mock())
        args = ['--project-name', 'functest', 'def']
        verifies = [('project_name', 'functest'), ('name', 'def')]
        parsed_args = self.check_parser(testcase_delete, args, verifies)
        testcase_delete.take_action(parsed_args)
        self.delete_mock.assert_called_once_with(
            self.base_url.format(parsed_args.project_name) + '/def',
            data=None,
            headers=clientmanager.ClientManager.headers)

    def test_delete_failure(self):
        with testtools.ExpectedException(Exception, 'Delete failed: Error'):
            self.delete_mock.return_value = utils.FAKE_FAILURE
            testcase_delete = testcases.TestcaseDelete(self.app, mock.Mock())
            args = ['--project-name', 'functest', 'def']
            verifies = [('project_name', 'functest'), ('name', 'def')]
            parsed_args = self.check_parser(testcase_delete, args, verifies)
            testcase_delete.take_action(parsed_args)


class TestcasePutTest(TestcaseTest):

    def setUp(self):
        super(TestcasePutTest, self).setUp()

    def test_put_success(self):
        self.put_mock.return_value = fakes.FakeResponse(
            data=self.testcase_json)
        testcase_put = testcases.TestcasePut(self.app, mock.Mock())
        args = ['--project-name', 'functest', 'def', self.testcase_string]
        verifies = [
            ('project_name', 'functest'),
            ('name', 'def'),
            ('testcase', self.testcase_json)]
        parsed_args = self.check_parser(testcase_put, args, verifies)
        testcase_put.take_action(parsed_args)
        self.put_mock.assert_called_once()

    def test_put_failure(self):
        with testtools.ExpectedException(Exception, 'Update failed: Error'):
            self.put_mock.return_value = utils.FAKE_FAILURE
            testcase_put = testcases.TestcasePut(self.app, mock.Mock())
            args = ['--project-name', 'functest', 'def', self.testcase_string]
            verifies = [
                ('project_name', 'functest'),
                ('name', 'def'),
                ('testcase', self.testcase_json)]
            parsed_args = self.check_parser(testcase_put, args, verifies)
            testcase_put.take_action(parsed_args)
