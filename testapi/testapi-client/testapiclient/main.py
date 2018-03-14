import sys

from cliff import app
from cliff import commandmanager

from testapiclient.utils import clientmanager


class TestAPIClient(app.App):

    def __init__(self):
        super(TestAPIClient, self).__init__(
            description='TestAPI Client',
            version='0.1',
            command_manager=commandmanager.CommandManager('testapi'),
            deferred_help=True,
        )

    def build_option_parser(self, description, version, argparse_kwargs=None):
        self.LOG.debug('build_option_parser')
        parser = super(TestAPIClient, self).build_option_parser(
            description,
            version,
            argparse_kwargs)
        parser.add_argument('-u',
                            type=str,
                            help='Username for authentication')
        parser.add_argument('-p',
                            type=str,
                            help='Password for authentication')
        return parser

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')
        self.client_manager = clientmanager.ClientManager(self.options)

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)
        if self.client_manager.auth_required:
            self.client_manager.auth()

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    client = TestAPIClient()
    return client.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
