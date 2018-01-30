import json
from user import User
from cliff.command import Command
from httpClient import HTTPClient


class TestCaseGet(Command):

    def get_parser(self, prog_name):
        parser = super(TestCaseGet, self).get_parser(prog_name)
        parser.add_argument('-project', type=str, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        TestCases = httpClient.get("http://localhost:8000/api/v1/projects/" + parsed_args.project + "/cases")
        print TestCases


class TestCaseCreate(Command):

    def get_parser(self, prog_name):
        parser = super(TestCaseCreate, self).get_parser(prog_name)
        parser.add_argument('-project', type=str, required=True)
        parser.add_argument('-case', type=json.loads, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        response = httpClient.post("http://localhost:8000/api/v1/projects/" + parsed_args.project + "/cases", User.session, parsed_args.case)
        if response.status_code == 200:
            print "TestCase has been successfully created!"
        else:
            print response.text


class TestCaseDelete(Command):

    def get_parser(self, prog_name):
        parser = super(TestCaseDelete, self).get_parser(prog_name)
        parser.add_argument('-project', type=str, required=True)
        parser.add_argument('-name', type=str, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        TestCases = httpClient.delete("http://localhost:8000/api/v1/projects/" + parsed_args.project + "/cases/" + parsed_args.name, User.session)
        print TestCases


class TestCasePut(Command):

    def get_parser(self, prog_name):
        parser = super(TestCasePut, self).get_parser(prog_name)
        parser.add_argument('-project', type=str, required=True)
        parser.add_argument('-name', type=str, required=True)
        parser.add_argument('-case', type=json.loads, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        TestCases = httpClient.put("http://localhost:8000/api/v1/projects/" + parsed_args.project + "/cases/" + parsed_args.name, User.session, parsed_args.case)
        print TestCases
