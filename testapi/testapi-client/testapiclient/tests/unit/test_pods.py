import StringIO

from mock import mock

from testapiclient.cli.pods import PodGet
from testapiclient.cli.pods import PodGetOne
from testapiclient.cli.pods import PodCreate
from testapiclient.cli.pods import PodDelete
from testapiclient.tests.unit import utils


class PodTest(utils.TestCommand):

    def setUp(self):
        super(PodTest, self).setUp()
        self.base_url = self.api_url + '/pods'
        self.pod_http_mock = mock.patch(
            'testapiclient.cli.pods.client.HTTPClient').start()
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


class PodGetTest(PodTest):

    def setUp(self):
        super(PodGetTest, self).setUp()

    def test_get(self):
        pod_get = PodGet(mock.Mock(), mock.Mock())
        arglist = ['-name', 'dfs']
        verifylist = [('name', 'dfs')]
        parsed_args = self.check_parser(pod_get, arglist, verifylist)
        pod_get.take_action(parsed_args)
        self.pod_http_mock.get_Instance().get.assert_called_once_with(
            self.base_url + '?name=dfs')

    def test_get_all(self):
        pod_get = PodGet(mock.Mock(), mock.Mock())
        arglist = []
        verifylist = []
        parsed_args = self.check_parser(pod_get, arglist, verifylist)
        pod_get.take_action(parsed_args)
        self.pod_http_mock.get_Instance().get.assert_called_once_with(
            self.base_url)

    def test_get_one(self):
        pod_get_one = PodGetOne(mock.Mock(), mock.Mock())
        arglist = ['def']
        verifylist = [('name', 'def')]
        parsed_args = self.check_parser(pod_get_one, arglist, verifylist)
        pod_get_one.take_action(parsed_args)
        self.pod_http_mock.get_Instance().get.assert_called_once_with(
            self.base_url + '/def')


class PodCreateTest(PodTest):

    def setUp(self):
        super(PodCreateTest, self).setUp()

    def test_create(self):
        pod_create = PodCreate(mock.Mock(), mock.Mock())
        arglist = [self.pod_string]
        verifylist = [
            ('pod', self.pod_json)
        ]
        parsed_args = self.check_parser(pod_create, arglist, verifylist)
        pod_create.take_action(parsed_args)
        self.pod_http_mock.get_Instance().post.assert_called_once_with(
            self.base_url,
            verifylist[0][1]
            )

    def test_create_success(self):
        with mock.patch('sys.stdout', new=StringIO.StringIO()) as mock_stdout:
            pod_create = PodCreate(mock.Mock(), mock.Mock())
            self.pod_http_mock.get_Instance().post.return_value.status_code \
                = 200
            arglist = [self.pod_string]

            verifylist = [
                ('pod', self.pod_json)
            ]
            parsed_args = self.check_parser(pod_create, arglist, verifylist)
            pod_create.take_action(parsed_args)
            self.assertEqual(
                mock_stdout.getvalue(),
                "Create success\n")

    def test_create_failure(self):
        with mock.patch('sys.stdout', new=StringIO.StringIO()) as mock_stdout:
            pod_create = PodCreate(mock.Mock(), mock.Mock())
            self.pod_http_mock.get_Instance().post.return_value.status_code\
                = 400
            self.pod_http_mock.get_Instance().post.return_value.reason = \
                "Error"
            arglist = [self.pod_string]

            verifylist = [
                ('pod', self.pod_json)
            ]
            parsed_args = self.check_parser(pod_create, arglist, verifylist)
            pod_create.take_action(parsed_args)
            self.assertEqual(mock_stdout.getvalue(), "Create failed: Error\n")

    def test_create_unauthorized(self):
        self.mock_unautherized()
        with mock.patch('sys.stdout', new=StringIO.StringIO()) as mock_stdout:
            with mock.patch('requests.Session') as mock_sessions:
                mock_sessions().post.return_value.text = "login"
                pod_create = PodCreate(mock.Mock(), mock.Mock())
                arglist = [
                    '-u', 'user', '-p', 'password', self.pod_string]
                verifylist = [
                    ('u', 'user'),
                    ('p', 'password'),
                    ('pod', self.pod_json)
                    ]
                parsed_args = self.check_parser(
                    pod_create,
                    arglist,
                    verifylist)
                pod_create.take_action(parsed_args)
                self.assertEqual(
                    mock_stdout.getvalue(),
                    "Authentication has failed.\n")

    def test_create_authorized(self):
        with mock.patch('requests.Session'):
            pod_create = PodCreate(mock.Mock(), mock.Mock())
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
            self.pod_http_mock.get_Instance().post.assert_called_once_with(
                self.base_url,
                verifylist[2][1]
                )


class PodDeleteTest(PodTest):

    def setUp(self):
        super(PodDeleteTest, self).setUp()

    def test_delete(self):
        pod_delete = PodDelete(mock.Mock(), mock.Mock())
        arglist = ['def']
        verifylist = [
            ('name', 'def')
        ]
        parsed_args = self.check_parser(pod_delete, arglist, verifylist)
        pod_delete.take_action(parsed_args)
        self.pod_http_mock.get_Instance().delete.assert_called_once_with(
            self.base_url + '/def',
            None
        )

    def test_delete_authorized(self):
        with mock.patch('requests.Session'):
            pod_delete = PodDelete(mock.Mock(), mock.Mock())
            arglist = [
                '-u', 'user', '-p', 'password', 'def'
            ]

            verifylist = [
                ('u', 'user'),
                ('p', 'password'),
                ('name', 'def')
            ]
            parsed_args = self.check_parser(pod_delete, arglist, verifylist)
            pod_delete.take_action(parsed_args)
            self.pod_http_mock.get_Instance().delete.assert_called_once_with(
                self.base_url + '/def',
                None
                )

    def test_delete_unauthorized(self):
        self.mock_unautherized()
        with mock.patch('sys.stdout', new=StringIO.StringIO()) as mock_stdout:
            with mock.patch('requests.Session') as mock_sessions:
                mock_sessions().post.return_value.text = "login"
                pod_delete = PodDelete(mock.Mock(), mock.Mock())
                arglist = [
                    '-u', 'user', '-p', 'password', 'def'
                ]

                verifylist = [
                    ('u', 'user'),
                    ('p', 'password'),
                    ('name', 'def')
                ]
                parsed_args = self.check_parser(
                    pod_delete,
                    arglist,
                    verifylist)
                pod_delete.take_action(parsed_args)
                self.assertEqual(
                    mock_stdout.getvalue(),
                    "Authentication has failed.\n")
