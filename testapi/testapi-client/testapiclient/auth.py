import logging
from cliff.command import Command
from testapiclient import identity


class Auth(Command):
    "Handle Authentication for users"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Auth, self).get_parser(prog_name)
        parser.add_argument('-u',
                            type=str,
                            required=True,
                            help='Username for authentication')
        parser.add_argument('-p',
                            type=str,
                            required=True,
                            help='Password for authentication')
        return parser

    def take_action(self, parsed_args):
        response = identity.authenticate(parsed_args.u, parsed_args.p)
        if "login" in response.text:
            print "Authentication has failed."
        else:
            print "Authentication has been successful!"
