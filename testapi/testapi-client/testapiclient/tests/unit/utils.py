import httplib

from mock import mock
from six.moves.urllib import parse
import testtools

from testapiclient.tests.unit import fakes
from testapiclient.utils import clientmanager

FAKE_FAILURE = fakes.FakeResponse(status_code=httplib.FORBIDDEN, data='Error')


class ParserException(Exception):
    pass


class TestCommand(testtools.TestCase):
    api_url = 'http://localhost:8000/api/v1/'

    def setUp(self):
        super(TestCommand, self).setUp()
        env_variables = {
            'testapi_url': 'http://localhost:8000/api/v1',
            'testapi_cas_auth_url':
            (
                'https://identity.linuxfoundation.org/user' +
                '/login?destination=cas/login%3Fservice%3D'
            ),
            'testapi_cas_signin_return': '/auth/signin_return'
        }
        self.config_mock = mock.patch.dict(
            'os.environ', env_variables).start()
        self.fake_stdout = fakes.FakeStdout()
        self.fake_log = fakes.FakeLog()
        self.app = fakes.FakeApp(self.fake_stdout, self.fake_log)
        self.app.client_manager = clientmanager.ClientManager()
        self.get_mock = mock.patch('requests.Session.get').start()
        self.post_mock = mock.patch('requests.Session.post').start()
        self.delete_mock = mock.patch('requests.Session.delete').start()
        self.put_mock = mock.patch('requests.Session.put').start()

    def check_parser(self, cmd, args, verify_args):
        cmd_parser = cmd.get_parser('check_parser')
        try:
            parsed_args = cmd_parser.parse_args(args)
        except SystemExit:
            raise ParserException("Argument parse failed")
        for av in verify_args:
            attr, value = av
            if attr:
                self.assertIn(attr, parsed_args)
                self.assertEqual(value, getattr(parsed_args, attr))
        return parsed_args

    def assert_url(self, actual_url, expected_url):
        actual_parsed = parse.parse_qs(parse.urlparse(actual_url).query)
        expected_parsed = parse.parse_qs(parse.urlparse(expected_url).query)
        assert actual_parsed == expected_parsed
