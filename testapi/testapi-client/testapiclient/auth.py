from testapiclient import command
from testapiclient import identity


class Auth(command.Command):
    "Handle Authentication for users"

    def get_parser(self, prog_name):
        parser = super(Auth, self).get_parser(prog_name)
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        print "Authentication has been successful!"
