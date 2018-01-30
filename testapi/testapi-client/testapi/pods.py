import json

from user import User
from cliff.command import Command
from httpClient import HTTPClient
from authHandler import AuthHandler


class PodGet(Command):
    "Handle get request for pods"

    def get_parser(self, prog_name):
        parser = super(PodGet, self).get_parser(prog_name)
        parser.add_argument('-name', default='', help='Search pods using name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        pods = httpClient.get("http://localhost:8000/api/v1/pods?name=" + parsed_args.name)
        print pods


class PodGetOne(Command):
    "Handle get request for pod by name"

    def get_parser(self, prog_name):
        parser = super(PodGetOne, self).get_parser(prog_name)
        parser.add_argument('-name', default='', help='Find pod using name', required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        pods = httpClient.get("http://localhost:8000/api/v1/pods/" + parsed_args.name)
        print pods


class PodCreate(Command):
    "Handle post request for pods"

    def get_parser(self, prog_name):
        parser = super(PodCreate, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('pod', type=json.loads, help='Pod create request format :{ "role": "community-ci" or "production-ci", "name": "", "details": "", "mode": "metal" or "virtual"}')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        response = httpClient.post("http://localhost:8000/api/v1/pods", User.session, parsed_args.pod)
        if response.status_code == 200:
            print "Pod has been successfully created!"
        else:
            print response.text


class PodDelete(Command):
    "Handle delete request for pods"

    def get_parser(self, prog_name):
        parser = super(PodDelete, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-name', type=str, required=True, help='Delete pods using name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        pods = httpClient.delete("http://localhost:8000/api/v1/pods/" + parsed_args.name, User.session)
        print pods
