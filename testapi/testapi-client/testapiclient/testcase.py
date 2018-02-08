import json
from user import User
from cliff.command import Command
from httpClient import HTTPClient
from authHandler import AuthHandler
from config import Config


class TestCaseBase(Command):
    projects_url = Config.config.get("api", "url") + "/projects/"


class TestCaseGet(TestCaseBase):

    def get_parser(self, prog_name):
        parser = super(TestCaseGet, self).get_parser(prog_name)
        parser.add_argument('-project', type=str, required=True, help='Get all testcases for a project name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        testCases = httpClient.get(TestCaseGet.projects_url + parsed_args.project + "/cases")
        print testCases


class TestCaseGetOne(TestCaseBase):

    def get_parser(self, prog_name):
        parser = super(TestCaseGetOne, self).get_parser(prog_name)
        parser.add_argument('-project', type=str, required=True, help='Get testcase for a project name')
        parser.add_argument('-name', type=str, required=True, help='Get a testcase by name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        testcase = httpClient.get(TestCaseGet.projects_url + parsed_args.project + "/cases/" + parsed_args.name)
        print testcase


class TestCaseCreate(TestCaseBase):

    def get_parser(self, prog_name):
        parser = super(TestCaseCreate, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-project', type=str, required=True, help='Create testcase under a project name')
        parser.add_argument('-case', type=json.loads, required=True, help='Testcase create request format:\n{"run": "", "name": "", "ci_loop": "", "tags": "",\n "url": "", "blocking": "", "domains": "", "dependencies": "",\n "version": "", "criteria": "", "tier": "", "trust": "",\n "catalog_description": "", "description": ""}')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        response = httpClient.post(TestCaseCreate.projects_url + parsed_args.project + "/cases", User.session, parsed_args.case)
        if response.status_code == 200:
            print "TestCase has been successfully created!"
        else:
            print response.text


class TestCaseDelete(TestCaseBase):

    def get_parser(self, prog_name):
        parser = super(TestCaseDelete, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-project', type=str, required=True, help='Delete testcase under project')
        parser.add_argument('-name', type=str, required=True, help='Delete testcase by name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        TestCases = httpClient.delete(TestCaseDelete.projects_url + parsed_args.project + "/cases/" + parsed_args.name, User.session)
        print TestCases


class TestCasePut(TestCaseBase):

    def get_parser(self, prog_name):
        parser = super(TestCasePut, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-project', type=str, required=True, help='Update the testcase under project')
        parser.add_argument('-name', type=str, required=True, help='Update the testcase by name')
        parser.add_argument('-case', type=json.loads, required=True, help='Testcase update request format:\n{"run": "", "name": "", "ci_loop": "", "tags": "",\n "url": "", "blocking": "", "domains": "", "dependencies": "",\n "version": "", "criteria": "", "tier": "", "trust": "",\n "catalog_description": "", "description": ""}')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        TestCases = httpClient.put(TestCasePut.projects_url + parsed_args.project + "/cases/" + parsed_args.name, User.session, parsed_args.case)
        print TestCases
