import StringIO
import httplib
import requests
import json
import testtools

from mock import mock
from six.moves.urllib import parse

from testapiclient.cli import pods
from testapiclient.tests.unit import utils
from testapiclient.utils import http_client
from testapiclient.utils import user


class PodTest(utils.TestCommand):
    def setUp(self):
        super(PodTest, self).setUp()
        user.User.session = requests.session()
        self.base_url = parse.urljoin(self.api_url, 'pods')
        self.pod_json = {
            'role': 'community-ci',
            'name': 'test_pod',
            'details': '',
            'mode': 'metal'
        }
        self.pod_string = json.dumps(self.pod_json)


class PodGetTest(PodTest):

    def setUp(self):
        super(PodGetTest, self).setUp()
        self.get_mock = mock.patch('requests.get').start()
        self.get_mock.return_value.status_code = httplib.OK

    def test_get(self):
        pod_get = pods.PodGet(mock.Mock(), mock.Mock())
        args = ['-name', 'dfs']
        verifies = [('name', 'dfs')]
        parsed_args = self.check_parser(pod_get, args, verifies)
        pod_get.take_action(parsed_args)
        self.get_mock.assert_called_once_with(
            self.base_url + '?name=dfs')

    def test_get_all(self):
        pod_get = pods.PodGet(mock.Mock(), mock.Mock())
        args = []
        verifies = []
        parsed_args = self.check_parser(pod_get, args, verifies)
        pod_get.take_action(parsed_args)
        self.get_mock.assert_called_once_with(
            self.base_url)

    def test_get_one(self):
        pod_get_one = pods.PodGetOne(mock.Mock(), mock.Mock())
        args = ['def']
        verifies = [('name', 'def')]
        parsed_args = self.check_parser(pod_get_one, args, verifies)
        pod_get_one.take_action(parsed_args)
        self.get_mock.assert_called_once_with(
            self.base_url + '/def')


class PodCreateTest(PodTest):

    def setUp(self):
        super(PodCreateTest, self).setUp()
        self.post_mock = mock.patch(
            'testapiclient.utils.user.User.session.post').start()
        self.post_mock.return_value.status_code = httplib.OK

    def test_create_success(self):
        pod_create = pods.PodCreate(mock.Mock(), mock.Mock())
        args = [self.pod_string]
        verifies = [('pod', self.pod_json)]
        parsed_args = self.check_parser(pod_create, args, verifies)
        pod_create.take_action(parsed_args)
        self.post_mock.assert_called_once()

    def test_create_failure(self):
        with testtools.ExpectedException(Exception, 'Create failed: Error'):
            pod_create = pods.PodCreate(mock.Mock(), mock.Mock())
            self.post_mock.return_value.status_code = httplib.BAD_REQUEST
            self.post_mock.return_value.reason = "Error"
            args = [self.pod_string]
            verifies = [('pod', self.pod_json)]
            parsed_args = self.check_parser(pod_create, args, verifies)
            pod_create.take_action(parsed_args)

    def test_create_unauthorized(self):
        self.mock_unautherized()
        with mock.patch('sys.stdout', new=StringIO.StringIO()) as mock_stdout:
            with mock.patch('requests.Session') as mock_sessions:
                mock_sessions().post.return_value.text = "login"
                pod_create = pods.PodCreate(mock.Mock(), mock.Mock())
                args = ['-u', 'user', '-p', 'password', self.pod_string]
                verifies = [
                    ('u', 'user'),
                    ('p', 'password'),
                    ('pod', self.pod_json)]
                parsed_args = self.check_parser(pod_create, args, verifies)
                pod_create.take_action(parsed_args)
                self.assertEqual(mock_stdout.getvalue(),
                                 "Authentication has failed.\n")

    def test_create_authorized(self):
        pod_create = pods.PodCreate(mock.Mock(), mock.Mock())
        args = ['-u', 'user', '-p', 'password', self.pod_string]
        verifies = [
            ('u', 'user'),
            ('p', 'password'),
            ('pod', self.pod_json)
        ]
        parsed_args = self.check_parser(pod_create, args, verifies)
        pod_create.take_action(parsed_args)
        self.post_mock.assert_called_once()


class PodDeleteTest(PodTest):

    def setUp(self):
        super(PodDeleteTest, self).setUp()
        self.delete_mock = mock.patch(
            'testapiclient.utils.user.User.session.delete').start()
        self.delete_mock.return_value.status_code = httplib.OK

    def test_delete_success(self):
        pod_delete = pods.PodDelete(mock.Mock(), mock.Mock())
        args = ['def']
        verifies = [('name', 'def')]
        parsed_args = self.check_parser(pod_delete, args, verifies)
        pod_delete.take_action(parsed_args)
        self.delete_mock.assert_called_once_with(
            self.base_url + '/def',
            data='null',
            headers=http_client.HTTPClient.headers)

    def test_delete_failure(self):
        with testtools.ExpectedException(Exception, 'Delete failed: Error'):
            pod_delete = pods.PodDelete(mock.Mock(), mock.Mock())
            self.delete_mock.return_value.status_code = httplib.FORBIDDEN
            self.delete_mock.return_value.reason = "Error"
            args = ['def']
            verifies = [('name', 'def')]
            parsed_args = self.check_parser(pod_delete, args, verifies)
            pod_delete.take_action(parsed_args)

    def test_delete_authorized(self):
        pod_delete = pods.PodDelete(mock.Mock(), mock.Mock())
        args = ['-u', 'user', '-p', 'password', 'def']
        verifies = [('u', 'user'), ('p', 'password'), ('name', 'def')]

        parsed_args = self.check_parser(pod_delete, args, verifies)
        pod_delete.take_action(parsed_args)
        self.delete_mock.assert_called_once_with(
            self.base_url + '/def',
            data='null',
            headers=http_client.HTTPClient.headers)

    def test_create_unauthorized(self):
        self.mock_unautherized()
        with mock.patch('sys.stdout', new=StringIO.StringIO()) as mock_stdout:
            with mock.patch('requests.Session') as mock_sessions:
                mock_sessions().post.return_value.text = "login"
                pod_delete = pods.PodDelete(mock.Mock(), mock.Mock())
                args = ['-u', 'user', '-p', 'password', 'def']
                verifies = [('u', 'user'), ('p', 'password'), ('name', 'def')]
                parsed_args = self.check_parser(pod_delete, args, verifies)
                pod_delete.take_action(parsed_args)
                self.assertEqual(mock_stdout.getvalue(),
                                 "Authentication has failed.\n")
