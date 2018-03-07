import json

from user import User
from cliff.command import Command
from httpClient import HTTPClient
from authHandler import AuthHandler
from config import Config


class PodBase(Command):
    pods_url = Config.config.get("api", "url") + "/pods"


class PodGet(PodBase):
    "Handle get request for pods"

    def get_parser(self, prog_name):
        parser = super(PodGet, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            help='Search pods using name')
        return parser

    def take_action(self, parsed_args):
        http_client = HTTPClient.get_Instance()
        url = PodGet.pods_url
        if(parsed_args.name):
            url = PodGet.pods_url + "?name=" + parsed_args.name
        pods = http_client.get(url)
        print pods


class PodGetOne(PodBase):
    "Handle get request for pod by name"

    def get_parser(self, prog_name):
        parser = super(PodGetOne, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            help='Find pod using name',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        http_client = HTTPClient.get_Instance()
        pods = http_client.get(PodGetOne.pods_url + "/" + parsed_args.name)
        print pods


class PodCreate(PodBase):
    "Handle post request for pods"

    def get_parser(self, prog_name):
        parser = super(PodCreate, self).get_parser(prog_name)
        parser.add_argument('-u',
                            type=str,
                            help='Username for authentication')
        parser.add_argument('-p',
                            type=str,
                            help='Password for authentication')
        parser.add_argument('pod',
                            type=json.loads,
                            help='Pod create request format :\n'
                                 '\'{"role": "", "name": "", "details": "", '
                                 '"mode": ""}\',\n role should be either '
                                 '"community-ci" or "production-ci", and '
                                 'mode should be either "metal" or "virtual.')
        return parser

    def take_action(self, parsed_args):
        http_client = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed."
                return
        response = http_client.post(PodCreate.pods_url,
                                    User.session,
                                    parsed_args.pod)
        if response.status_code == 200:
            print "Pod has been successfully created!"
        else:
            print response.text


class PodDelete(PodBase):
    "Handle delete request for pods"

    def get_parser(self, prog_name):
        parser = super(PodDelete, self).get_parser(prog_name)
        parser.add_argument('-u',
                            type=str,
                            help='Username for authentication')
        parser.add_argument('-p',
                            type=str,
                            help='Password for authentication')
        parser.add_argument('-name',
                            type=str,
                            required=True,
                            help='Delete pods using name')
        return parser

    def take_action(self, parsed_args):
        http_client = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed."
                return
        pods = http_client.delete(PodDelete.pods_url + "/" + parsed_args.name,
                                  User.session)
        print pods
