from mock import mock
from testapiclient.pods import PodGet
from testapiclient.pods import PodGetOne
from testapiclient.pods import PodCreate
from testapiclient.pods import PodDelete
import StringIO
from utils import TestCommand


class PodTest(TestCommand):
    api_url = 'http://localhost:8000/api/v1'
    base_url = 'http://localhost:8000/api/v1/pods'

    def setUp(self):
        super(PodTest, self).setUp()
        self.config_mock = mock.patch('testapiclient.pods.Config').start()
        self.config_mock.get_Instance().get_conf().get.return_value \
            = self.api_url
        self.pod_string = '''{ "role": "community-ci",
        "name": "test_pod",
        "details": "",
        "mode": "metal"}'''
        self.pod_json = {
            u'role': u'community-ci',
            u'name': u'test_pod',
            u'details': u'',
            u'mode': u'metal'
            }

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_get(self, pod_get_http_mock):
        pod_get = PodGet(mock.Mock(), mock.Mock())
        arglist = ['-name', 'dfs']
        verifylist = [('name', 'dfs')]
        parsed_args = self.check_parser(pod_get, arglist, verifylist)
        pod_get.take_action(parsed_args)
        pod_get_http_mock.get_Instance().get.assert_called_once_with(
            self.base_url + '?name=dfs')

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_get_all(self, pod_get_http_mock):
        pod_get = PodGet(mock.Mock(), mock.Mock())
        arglist = []
        verifylist = []
        parsed_args = self.check_parser(pod_get, arglist, verifylist)
        pod_get.take_action(parsed_args)
        pod_get_http_mock.get_Instance().get.assert_called_once_with(
            self.base_url)

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_get_one(self, pod_get_http_mock):
        pod_get_one = PodGetOne(mock.Mock(), mock.Mock())
        arglist = ['-name', 'def']
        verifylist = [('name', 'def')]
        parsed_args = self.check_parser(pod_get_one, arglist, verifylist)
        pod_get_one.take_action(parsed_args)
        pod_get_http_mock.get_Instance().get.assert_called_once_with(
            self.base_url + '/def')

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_create(self, pod_create_http_mock):
        pod_create = PodCreate(mock.Mock(), mock.Mock())
        arglist = [self.pod_string]

        verifylist = [
            ('pod', self.pod_json)
        ]
        parsed_args = self.check_parser(pod_create, arglist, verifylist)
        pod_create.take_action(parsed_args)
        pod_create_http_mock.get_Instance().post.assert_called_once_with(
            self.base_url,
            None,
            verifylist[0][1]
            )

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_create_success(self, pod_create_http_mock):
        with mock.patch('sys.stdout', new=StringIO.StringIO()) as mock_stdout:
            pod_create = PodCreate(mock.Mock(), mock.Mock())
            pod_create_http_mock.get_Instance().post.return_value.status_code \
                = 200
            arglist = [self.pod_string]

            verifylist = [
                ('pod', self.pod_json)
            ]
            parsed_args = self.check_parser(pod_create, arglist, verifylist)
            pod_create.take_action(parsed_args)
            self.assertEqual(
                mock_stdout.getvalue(),
                "Pod has been successfully created!\n")

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_create_failure(self, pod_create_http_mock):
        with mock.patch('sys.stdout', new=StringIO.StringIO()) as mock_stdout:
            pod_create = PodCreate(mock.Mock(), mock.Mock())
            pod_create_http_mock.get_Instance().post.return_value.status_code\
                = 400
            pod_create_http_mock.get_Instance().post.return_value.text = \
                "Error"
            arglist = [self.pod_string]

            verifylist = [
                ('pod', self.pod_json)
            ]
            parsed_args = self.check_parser(pod_create, arglist, verifylist)
            pod_create.take_action(parsed_args)
            self.assertEqual(mock_stdout.getvalue(), "Error\n")

    @mock.patch('testapiclient.pods.AuthHandler')
    @mock.patch('testapiclient.pods.HTTPClient')
    def test_create_unauthorized(self, pod_create_http_mock, pod_auth):
        pod_create = PodCreate(mock.Mock(), mock.Mock())
        pod_auth.authenticate.return_value.text = 'login'
        arglist = [
            '-u', 'user', '-p', 'password', self.pod_string]

        verifylist = [
            ('u', 'user'),
            ('p', 'password'),
            ('pod', self.pod_json)
            ]
        parsed_args = self.check_parser(pod_create, arglist, verifylist)
        pod_create.take_action(parsed_args)
        pod_create_http_mock.get_Instance().post.assert_not_called()

    @mock.patch('testapiclient.pods.AuthHandler')
    @mock.patch('testapiclient.pods.HTTPClient')
    def test_create_authorized(self, pod_create_http_mock, pod_auth):
        pod_create = PodCreate(mock.Mock(), mock.Mock())
        pod_auth.authenticate.return_value.text = 'success'
        arglist = [
            '-u', 'user', '-p', 'password',
            self.pod_string
        ]

        verifylist = [
            ('u', 'user'),
            ('p', 'password'),
            ('pod', self.pod_json)
        ]
        parsed_args = self.check_parser(pod_create, arglist, verifylist)
        pod_create.take_action(parsed_args)
        pod_create_http_mock.get_Instance().post.assert_called_once_with(
            self.base_url,
            None,
            verifylist[2][1]
            )

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_delete(self, pod_delete_http_mock):
        pod_delete = PodDelete(mock.Mock(), mock.Mock())
        arglist = ['-name', 'def']
        verifylist = [
            ('name', 'def')
        ]
        parsed_args = self.check_parser(pod_delete, arglist, verifylist)
        pod_delete.take_action(parsed_args)
        pod_delete_http_mock.get_Instance().delete.assert_called_once_with(
            self.base_url + '/def',
            None
            )

    @mock.patch('testapiclient.pods.AuthHandler')
    @mock.patch('testapiclient.pods.HTTPClient')
    def test_delete_unauthorized(self, pod_delete_http_mock, pod_auth):
        pod_auth.authenticate.return_value.text = 'login'
        pod_delete = PodDelete(mock.Mock(), mock.Mock())
        arglist = [
            '-u', 'user', '-p', 'password', '-name', 'def'
        ]

        verifylist = [
            ('u', 'user'),
            ('p', 'password'),
            ('name', 'def')
        ]
        parsed_args = self.check_parser(pod_delete, arglist, verifylist)
        pod_delete.take_action(parsed_args)
        pod_delete_http_mock.get_Instance().delete.assert_not_called()

    @mock.patch('testapiclient.pods.AuthHandler')
    @mock.patch('testapiclient.pods.HTTPClient')
    def test_delete_authorized(self, pod_delete_http_mock, pod_auth):
        pod_auth.authenticate.return_value.text = 'success'
        pod_delete = PodDelete(mock.Mock(), mock.Mock())
        arglist = [
            '-u', 'user', '-p', 'password', '-name', 'def'
        ]

        verifylist = [
            ('u', 'user'),
            ('p', 'password'),
            ('name', 'def')
        ]
        parsed_args = self.check_parser(pod_delete, arglist, verifylist)
        pod_delete.take_action(parsed_args)
        pod_delete_http_mock.get_Instance().delete.assert_called_once_with(
            self.base_url + '/def',
            None
            )
