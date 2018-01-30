import requests
from user import User
import logging
from cliff.command import Command


class Auth(Command):
    "Handle Authentication for users"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Auth, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, required=True)
        parser.add_argument('-p', type=str, required=True)
        return parser

    def take_action(self, parsed_args):
        self.session = requests.Session()
        # self.hostname = "https://identity.linuxfoundation.org/user/login?destination=cas/login%3Fservice%3Dhttp%253A//testresults.opnfv.org/test/api/v1/auth/signin_return"
        self.hostname = "https://identity.linuxfoundation.org/user/login?destination=cas/login%3Fservice%3Dhttp%253A//localhost%253A8000/api/v1/auth/signin_return"
        self.data = {'name': parsed_args.u, 'pass': parsed_args.p, 'form_id': 'user_login'}
        self.response = self.session.post(self.hostname, self.data)
        User.session = self.session
        if "login" in self.response.text:
            print "Authentication has failed. Please check your username and password."
        else:
            print "Authentication has been successful!"
        return self.session
