import testtools
from mock import mock

from testapiclient.utils.user import User


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

    def mock_unautherized(self):
        User.session = None
