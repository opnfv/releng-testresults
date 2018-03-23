import json

from mock import mock
from six.moves.urllib import parse

from testapiclient.cli import scenarios
from testapiclient.tests.unit import fakes
from testapiclient.tests.unit import utils


class ProjectTest(utils.TestCommand):
    def setUp(self):
        super(ProjectTest, self).setUp()
        self.base_url = parse.urljoin(self.api_url, 'scenarios/{}/projects')
        self.scenario_name = 's1'
        self.project_json = {
            'trust_indicators': [],
            'project': 'test-project',
            'scores': [],
            'customs': []
        }
        self.project_string = json.dumps(self.project_json)


class ProjectCreateTest(ProjectTest):

    def setUp(self):
        super(ProjectCreateTest, self).setUp()

    def test_create_success(self):
        self.post_mock.return_value = fakes.FakeResponse(data=None)
        project_create = scenarios.ProjectCreate(self.app, mock.Mock())
        args = [
            '--scenario-name', 's1', '--installer', 'i1', '--version', 'v1',
            self.project_string]
        verifies = [
            ('scenario_name', 's1'),
            ('installer', 'i1'),
            ('version', 'v1'),
            ('project', self.project_json)]
        parsed_args = self.check_parser(project_create, args, verifies)
        project_create.take_action(parsed_args)
        self.post_mock.assert_called_once()


class ProjectDeleteTest(ProjectTest):

    def setUp(self):
        super(ProjectDeleteTest, self).setUp()

    def test_delete_success(self):
        self.delete_mock.return_value = fakes.FakeResponse(data=None)
        project_delete = scenarios.ProjectDelete(self.app, mock.Mock())
        args = [
            '--scenario-name', 's1', '--installer', 'i1', '--version', 'v1',
            'def']
        verifies = [
            ('scenario_name', 's1'),
            ('installer', 'i1'),
            ('version', 'v1'),
            ('name', ['def'])]
        parsed_args = self.check_parser(project_delete, args, verifies)
        project_delete.take_action(parsed_args)
        kall = self.delete_mock.call_args
        args, kwargs = kall
        self.assert_url(
            args[0],
            self.base_url + '?version=v1&installer=i1')


class ProjectPutTest(ProjectTest):

    def setUp(self):
        super(ProjectPutTest, self).setUp()

    def test_put_success(self):
        self.put_mock.return_value = fakes.FakeResponse(
            data=None)
        project_put = scenarios.ProjectPut(self.app, mock.Mock())
        args = [
            '--scenario-name', 's1', '--installer', 'i1', '--version', 'v1',
            self.project_string]
        verifies = [
            ('scenario_name', 's1'),
            ('installer', 'i1'),
            ('version', 'v1'),
            ('project', self.project_json)]
        parsed_args = self.check_parser(project_put, args, verifies)
        project_put.take_action(parsed_args)
        self.put_mock.assert_called_once()
